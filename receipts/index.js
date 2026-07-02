const express = require('express');
const app = express();
app.use(express.json());

app.post('/receipt', (req, res) => {
    const { name, price, amount } = req.body;
    const time = new Date().toISOString();
    
    const receipt = `
================================
         VENDING MACHINE
================================
Item    : ${name}
Price   : Rp${price}
Amount  : ${amount}
Time    : ${time}
================================
  Thank You for Your Purchase!
================================`;
    
    res.json({ receipt });
});

app.listen(3000, () => console.log('Receipt service running on port 3000'));