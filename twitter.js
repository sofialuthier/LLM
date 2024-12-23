require('dotenv').config();
const { TwitterApi } = require('twitter-api-v2');

const client = new TwitterApi(process.env.TWITTER_BEARER_TOKEN);

/**
 * Belirli bir konuyla ilgili tweetleri çeker
 * @param {string} topic - Aranacak konu
 * @returns {Promise<void>}
 */
async function fetchTweetsByTopic(topic) {
    let nextToken = null;
    let attempts = 0; // Hata durumunda yeniden deneme sayısı

    // En fazla 100 tweet'e kadar sınırlıyoruz
    for (let i = 0; i < 10; i++) {
        try {
            const params = {
                'tweet.fields': 'created_at,lang,author_id',
                max_results: 10,
                next_token: nextToken,
            };

            const tweets = await client.v2.search(topic, params);

            if (tweets.data && tweets.data.data) {
                tweets.data.data.forEach((tweet, index) => {
                    console.log(`\nTweet #${index + 1}`);
                    console.log(`User ID: ${tweet.author_id}`);
                    console.log(`Created at: ${tweet.created_at}`);
                    console.log(`Tweet: ${tweet.text}`);
                    console.log('-----------------------------');
                });

                nextToken = tweets.data.meta?.next_token;
                if (!nextToken) break;
            } else {
                console.log('No tweets found for this topic.');
                break;
            }

            // Rate limit aşmamak için her isteğin ardından 1 saniye bekle
            await new Promise(resolve => setTimeout(resolve, 1000));
        } catch (error) {
            console.error('Error fetching tweets:', error);

            // Eğer hata 429 ise (rate limit aşıldıysa) bekle ve tekrar dene
            if (error.code === 429) {
                const resetTime = error.rateLimit?.reset * 1000;
                const waitTime = resetTime ? resetTime - Date.now() : 60 * 1000;
                console.log(`Rate limit reached. Waiting for ${waitTime / 1000} seconds...`);

                // Bekleme süresi kadar bekle
                await new Promise(resolve => setTimeout(resolve, waitTime));
                attempts++;
                
                // Çok fazla deneme yapıldıysa işlemi sonlandır
                if (attempts > 3) {
                    console.error('Too many attempts. Exiting...');
                    break;
                }
            } else {
                console.error('Unexpected error:', error);
                break;
            }
        }
    }
}

module.exports = { fetchTweetsByTopic };
