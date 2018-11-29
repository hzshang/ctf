import React from 'react';
import { Row, Divider, Button } from 'antd';
import Cards from 'react-credit-cards';

function CardsList(props) {
  const cards = props.cards;
  const holderName = props.holderName;
  const accountNumber = props.accountNumber;

  function handlePaymentFrom(from, fromType, to, toType) {
    props.showPaymentModal(from, fromType, to, toType);
  }

  const listItems = cards.map((card) =>
    <div>
      <Divider />
      <div style={{float: 'right', paddingRight: 26, textAlign: 'center'}}>
        <h3>${card.balance}</h3>
        <Row style={{paddingBottom: 5}}>
          <Button
            style={{'width': 50}}
            size="large"
            className="card-button-blue"
            icon="double-right"
            onClick={()=>handlePaymentFrom(card.id, 'Card', null, null)}
          >
          </Button>
        </Row>
        <Row style={{paddingBottom: 5}}>
          <Button
            style={{'width': 50}}
            className="card-button-green"
            size="large"
            icon="double-left"
            onClick={()=>handlePaymentFrom(accountNumber, 'Account', card.id, 'Card')}
          >
          </Button>
        </Row>
        <Row style={{paddingBottom: 5}}>
          <a href={'/api/report/?Card=' + card.id}><Button
            style={{'width': 50}}
            className="card-button-red"
            size="large"
            icon="download"
          >
          </Button></a>
        </Row>
      </div>
      <div style={{display: 'inline-block', paddingRight: 25}}>
        <Cards
          number={card.id}
          name={holderName}
          expiry='1122'
          cvc='XXX'
        />
      </div>
      <div style={{display: 'inline-block'}}>
        <Cards
          number={card.id}
          name={holderName}
          expiry='1122'
          cvc='XXX'
          focused='cvc'
        />
      </div>
    </div>
  );
  return (
    <div>{listItems}</div>
  );
}

export default CardsList;