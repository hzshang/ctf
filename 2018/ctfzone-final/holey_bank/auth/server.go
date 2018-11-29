package main

import (
    bio "Web/auth/bio_service"
    "fmt"
    "github.com/go-pg/pg"
    "github.com/go-pg/pg/orm"
    "golang.org/x/crypto/bcrypt"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
    "log"
    "net"
    "time"
)

const port = 7777

type IdentityStorageServer struct {
    DB *pg.DB
}

func HashPassword(password string) (string, error) {
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), 10)
    return string(bytes), err
}

func CheckPasswordHash(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}


func (s *IdentityStorageServer) Register(ctx context.Context, auth *bio.Authentication) (*bio.Response, error) {

    var authInDB []bio.Authentication
    var resp bio.Response
    var db = s.DB

    exists, err := db.Model(&authInDB).Where("username = ?", auth.Username).Exists()

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Error connecting to DB: %s", err)
    }

    if exists {
        resp.Result = false
        resp.Message = "User already exists"
        return &resp, nil
    }

    hash, _ := HashPassword(auth.Password)
    auth.Password = hash

    err = db.Insert(auth)

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Could not insert item into the database: %s", err)
    }

    resp.Result = true
    resp.Message = "Ok"
    return &resp, nil

}

func (s *IdentityStorageServer) Authenticate(ctx context.Context, auth *bio.Authentication) (*bio.Response, error) {
    var authInDB bio.Authentication
    var resp bio.Response
    var db = s.DB

    err := db.Model(&authInDB).Where("username = ?", auth.Username).First()

    if err == pg.ErrNoRows {
        resp.Message = "No such user"
        resp.Result = false
        return &resp, nil
    }

    if err != nil {
        return nil, status.Errorf(codes.NotFound, "Could not retrieve item from the database: %s", err)
    }

    match := CheckPasswordHash(auth.Password, authInDB.Password)

    if match {
        resp.Message = "Ok"
        resp.Result = true
    } else {
        resp.Message = "Incorrect password"
        resp.Result = false
    }

    return &resp, nil
}

func (s *IdentityStorageServer) SetInfo(ctx context.Context, identity *bio.Identity) (*bio.Response, error) {
    var resp bio.Response
    var db = s.DB
    var auth = identity.Authentication
    var authInDB bio.Authentication
    var passportInDB bio.Passport

    if identity.Authentication == nil {
        resp.Message = "No authentication provided"
        resp.Result = false
        return &resp, nil
    }

    if identity.Passport == nil {
        resp.Message = "No passport provided"
        resp.Result = false
        return &resp, nil
    }

    exists, err := db.Model(&authInDB).Where("username = ?", auth.Username).Exists()

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Error connecting to DB: %s", err)
    }

    if exists {
        resp.Result = false
        resp.Message = "User already exists"
        return &resp, nil
    }

    exists, err = db.Model(&passportInDB).Where("passport_number = ?", identity.Passport.PassportNumber).Exists()

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Error connecting to DB: %s", err)
    }

    if exists {
        resp.Result = false
        resp.Message = "Passport already exists"
        return &resp, nil
    }


    hash, _ := HashPassword(auth.Password)
    auth.Password = hash

    err = db.Insert(auth)

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Could not insert item into the database: %s", err)
    }

    err = db.Model(&authInDB).Where("username = ?", auth.Username).First()

    if err == pg.ErrNoRows {
        resp.Message = "Error creating user"
        resp.Result = false
        return &resp, nil
    }

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Error connecting to DB: %s", err)
    }

    identity.AuthenticationId = authInDB.Id

    err = db.Insert(identity.Passport)

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Can not insert Passport into the database: %s", err)
    }

    identity.PassportId = identity.Passport.Id

    err = db.Insert(identity)

    if err != nil {
        return nil, status.Errorf(codes.Internal, "Can not insert Identity into the database: %s", err)
    }

    resp.Result = true
    resp.Message = "Ok"

    return &resp, nil
}

func (s *IdentityStorageServer) GetInfoByAuthentication(ctx context.Context, auth *bio.Authentication) (*bio.Identity, error) {
    identity := new(bio.Identity)
    var db = s.DB
    var authInDB bio.Authentication

    err := db.Model(&authInDB).Where("username = ?", auth.Username).First()

    if err == pg.ErrNoRows {
        return nil, err
    }

    err = db.Model(identity).Column("identity.*","Authentication", "Passport").Where("authentication_id = ?", authInDB.Id).Select()

    if err == pg.ErrNoRows {
        return nil, err
    }

    return identity, nil
}

func (s *IdentityStorageServer) GetInfo(ctx context.Context, identityID *bio.IdentityId) (*bio.Identity, error) {
    identity := new(bio.Identity)
    var db = s.DB

    err := db.Model(identity).Column("identity.*","Authentication", "Passport").Where("identity.authentication_id = ?", identityID.Id).Select()

    if err == pg.ErrNoRows {
        return nil, err
    }

    if err != nil {
        return nil, err
    }

    return identity, nil
}

func (s *IdentityStorageServer) GetAllUsers(ctx context.Context, _ *bio.None) (*bio.Authentications, error) {
    authentications := new(bio.Authentications)
    var db = s.DB

    err := db.Model(&authentications.Authentications).Select()

    if err != nil {
        return nil, err
    }

    return authentications, nil
}



func main() {

    db := pg.Connect(&pg.Options{
        User:     "identity_storage",
        Password: "identity_storage",
        Database: "storage",
        Addr:     "db:5432",
    })
    defer db.Close()

    var err error

    for err = db.CreateTable(&bio.Authentication{}, &orm.CreateTableOptions{
        FKConstraints: true,
        IfNotExists: true,
    }); err != nil;{
        log.Println("Waiting for DB container")
        time.Sleep(5 * time.Second)
        err = db.CreateTable(&bio.Authentication{}, &orm.CreateTableOptions{
            FKConstraints: true,
            IfNotExists: true,
        })

    } //Waiting till DB starts

    db.CreateTable(&bio.Passport{}, &orm.CreateTableOptions{
        FKConstraints: true,
        IfNotExists: true,
    })

    if err != nil {
        log.Fatalf("Error creating table! %v", err)
    }

    db.CreateTable(&bio.Identity{}, &orm.CreateTableOptions{
        FKConstraints: true,
        IfNotExists: true,
    })

    if err != nil {
        log.Fatalf("Error creating table! %v", err)
    }

    lis, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    grpcServer := grpc.NewServer()
    serv := &IdentityStorageServer{DB: db}
    bio.RegisterIdentityStorageServer(grpcServer, serv)
    grpcServer.Serve(lis)

}