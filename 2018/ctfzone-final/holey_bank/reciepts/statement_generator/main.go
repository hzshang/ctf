package main

import (
    "bytes"
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "io/ioutil"
    "math/rand"
    "net/http"
    "os"
    "os/exec"
    "text/template"
    "time"
)

var (
    idgwHost = "identity_storage"
    idgwPort = "8080"
    idgwPath = "/v1/authentication_get_info"
    dbHost = "processing"
    dbDatabase = "Processing"
    dbUsername = "processing"
    dbPassword = "ALKHsd871gekag8J*@!&YTEOIEY^!@#"
)

var db *sql.DB

type Transaction struct {
    From string
    To string
    Date time.Time
    Sum int
    Comment string
    FromMe bool
}

type Authenication struct {
    Username string `json:"username"`
    Password string `json:"password"`
}

type Passport struct {
    FullName string `json:"full_name"`
    Residence string `json:"residence"`
    PassportNumber int `json:"passport_number"`
}

type Identity struct {
    Authentication Authenication `json:"authentication"`
    Passport Passport `json:"passport"`
}

type Content struct {
    Program string
    Username string
    Identity Identity
    Card string
    Theme string
    Transactions []Transaction
    Total int
}

func init() {
    rand.Seed(time.Now().UnixNano())
}

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

func genRandString(n int) string {
    b := make([]byte, n)
    for i := range b {
        b[i] = letterBytes[rand.Intn(len(letterBytes))]
    }
    return string(b)
}

func getTransactions(subject string) (error, []Transaction) {
    stmt, err := db.Prepare("select from_, to_, sum, transfer_comment from Transactions where from_=? or to_=?")
    if err != nil {
        return err, nil
    }

    var transactions []Transaction

    res, err := stmt.Query(subject, subject)
    if err != nil {
        defer stmt.Close()
        return err, nil
    }

    for res.Next() {
        var transaction Transaction
        err = res.Scan(&transaction.From, &transaction.To, &transaction.Sum, &transaction.Comment)
        if err != nil {
            defer stmt.Close()
            return err, nil
        }
        transactions = append(transactions, transaction)
    }
    defer stmt.Close()
    return nil, transactions
    
}

func generatePdf (content *Content) (error, string) {
    t, err := template.ParseFiles("welcome.html")

    randString := genRandString(10)

    f, err := os.Create("tpl.html." + randString)
    if err != nil {
        return err, ""
    }

    err = t.Execute(f, struct{Theme string}{content.Theme})

    if err != nil {
        return err, ""
    }

    f.Close()

    t, err = template.ParseFiles("tpl.html." + randString)
    if err != nil {
        return err, ""
    }

    outputFile := "out." + randString

    f2, err := os.Create(outputFile + ".html")
    if err != nil {
        return err, ""
    }

    err = t.Execute(f2, content)
    if err != nil {
        return err, ""
    }
    f2.Close()

    err = exec.Command("bash", "-c", content.Program + outputFile + ".html " + outputFile + ".pdf").Run()

    if err != nil {
        return err, ""
    }

    //Cleanup
    err = os.Remove(outputFile + ".html")
    if err != nil {
        return err, ""
    }
    err = os.Remove("tpl.html." + randString)
    if err != nil {
        return err, ""
    }

    return nil, outputFile + ".pdf"

}

func getIdentity(auth string) (error, *Identity) {
    resp, err := http.Post("http://" + idgwHost + ":" + idgwPort + idgwPath, "application/x-www-form-urlencoded", bytes.NewBuffer([]byte("{\"username\":\"" + auth + "\"}")))
    if err != nil {
        return err, nil
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return err, nil
    }
    id := new(Identity)

    err = json.Unmarshal(body, id)
    if err != nil {
        return err, nil
    }

    return nil, id
}

func handleRequest(req string) (string, error) {
    content := new(Content)
    content.Program = "wkhtmltopdf "
    err := json.Unmarshal([]byte(req), content)
    if err != nil {
        return "", err
    }

    subject := content.Card
    err, transactions := getTransactions(subject)
    if err != nil {
        return "", err
    }


    sum := 0
    for i, transaction := range transactions {
        if transaction.To == content.Card {
            transactions[i].FromMe = false
            sum += transaction.Sum
        } else {
            transactions[i].FromMe = true
            sum -= transaction.Sum
        }
    }

    content.Transactions = transactions
    content.Total = sum

    if err, id := getIdentity(content.Username); err != nil {
        return "", err
    } else {
        content.Identity = *id
    }

    err, fileName := generatePdf(content)

    if err != nil {
        return "", err
    }

    return fileName, nil
}

func handler(w http.ResponseWriter, r *http.Request) {
    
    if r.Method != "POST" {
        http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
        return
    }

    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading request body",
            http.StatusInternalServerError)
        return
    }

    fileName, err := handleRequest(string(body))

    if err != nil {
        http.Error(w, err.Error(),
            http.StatusInternalServerError)
        return
    }

    http.ServeFile(w, r, fileName)
    os.Remove(fileName)
    
}

func main() {
    var err error
    db, err = sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?charset=utf8",dbUsername, dbPassword,
        dbHost, dbDatabase))
    if err != nil {
        fmt.Printf("Error connecting to SQL. %v", err)
        return
    }
    http.HandleFunc("/generateStatement", handler)
    http.ListenAndServe(":8081", nil)

}












