const express = require('express');
const fs = require('fs');
const readline = require('readline');
const path = require('path');
const cors = require('cors');

const app = express();

app.use(cors());
var corsOptions = {
  origin: '*',
  optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
}
app.use(cors(corsOptions))
const port = 4000;

const readTokenFile = async(chatTokenPath, counterPath) => {
    let counter = fs.readFileSync(counterPath, 'utf-8');
    counter = Number(counter);

    const readInterface = readline.createInterface({
        input: fs.createReadStream(chatTokenPath),
        console: false
    });

    let lineCount = 0;
    for await(const line of readInterface) {
        if (lineCount === counter) {
            counter++;
            fs.writeFileSync(counterPath, counter.toString());

            readInterface.close(); // Close the readline interface
            return line;
        }
        lineCount++;
    }

    // If  reach here,have read all lines, reset counter and call this function again
    counter = 0;
    fs.writeFileSync(counterPath, counter.toString());
    return await readTokenFile(chatTokenPath, counterPath);
};

app.post('/api/authorization', async(req, res) => {
    const chatTokenPath = path.join(__dirname, 'Data', 'chat_token_fake.txt');
    const counterPath = path.join(__dirname, 'Data', 'counter.txt');

    try {
        const token = await readTokenFile(chatTokenPath, counterPath);
        res.send({
            token: token
        });
    } catch (error) {
        // If reach here, something went wrong
        res.status(500).send({
            message: 'Unexpected error occurred.'
        });
    }
});
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});