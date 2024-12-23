// Twitter API ile tweetleri almak için gerekli kütüphaneler
const axios = require('axios');
require('dotenv').config();

// Twitter API ayarları
const BEARER_TOKEN = process.env.TWITTER_ACCESS_TOKEN;

// Ekonomi ile ilgili tweetleri almak için fonksiyon
const getEconomyTweets = async () => {
  const query = 'economy'; // Ekonomi konusundaki tweetler
  const url = `https://api.twitter.com/2/tweets/search/recent?query=${query}&max_results=10`; // Son 10 tweet

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${BEARER_TOKEN}`,
      },
    });

    // Tweetleri ekrana yazdırma
    const tweets = response.data.data;
    if (tweets) {
      console.log('Economy-related Tweets:');
      tweets.forEach(tweet => {
        console.log(`- ${tweet.text}`);
      });
    } else {
      console.log('No tweets found.');
    }
  } catch (error) {
    console.error('Error fetching tweets:', error);
  }
};

// Fonksiyonu çağırarak tweetleri alalım
getEconomyTweets();
const getRateLimitInfo = (response) => {
  const limit = response.headers['x-rate-limit-limit'];
  const remaining = response.headers['x-rate-limit-remaining'];
  const resetTime = response.headers['x-rate-limit-reset'];

  console.log(`Limit: ${limit}`);
  console.log(`Remaining: ${remaining}`);
  console.log(`Reset Time: ${resetTime}`);

  return { remaining, resetTime };
};

const getEconomyTweetsWithRateLimitCheck = async () => {
  const query = 'siyaset'; // Ekonomi konusundaki tweetler
  const url = `https://api.twitter.com/2/tweets/search/recent?query=${query}&max_results=10`;

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${BEARER_TOKEN}`,
      },
    });

    // Rate limit bilgisini kontrol et
    const { remaining, resetTime } = getRateLimitInfo(response);

    // Eğer rate limit aşılmışsa, bekle ve yeniden dene
    if (remaining === 0) {
      const currentTime = Math.floor(Date.now() / 1000);
      const waitTime = resetTime - currentTime + 1;

      console.log(`Rate limit aşıldı, bekleme süresi: ${waitTime} saniye`);
      await new Promise(resolve => setTimeout(resolve, waitTime * 1000)); // Bekleme süresi
      return getEconomyTweetsWithRateLimitCheck(); // Yeniden dene
    }

    // Tweetleri yazdır
    const tweets = response.data.data;
    if (tweets) {
      console.log('Economy-related Tweets:');
      tweets.forEach(tweet => {
        console.log(`- ${tweet.text}`);
      });
    } else {
      console.log('No tweets found.');
    }
  } catch (error) {
    console.error('Error fetching tweets:', error);
  }
};

// Fonksiyonu çağır
getEconomyTweetsWithRateLimitCheck();
