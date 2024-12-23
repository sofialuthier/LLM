const { fetchTweetsByTopic } = require('./twitter');

const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Kullanıcıdan bir konu istemek için
rl.question('Please enter a topic to search for tweets: ', async (topic) => {
    await fetchTweetsByTopic(topic);
    rl.close();
});
