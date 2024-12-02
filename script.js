const searchButton = document.getElementById("search-btn");
const cityInput = document.getElementById("city-input");
const weatherInfo = document.getElementById("weather-info");

const apiKey = "d66c2caafa759a2cca2d8ab041abcd52"; // Your actual API key from OpenWeatherMap

// Function to fetch weather data
const getWeather = async (city) => {
  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
    );
    const data = await response.json();

    if (data.cod === "404") {
      weatherInfo.innerHTML = `<p>City not found!</p>`;
    } else {
      const { main, weather, wind } = data;
      const temperature = main.temp;
      const description = weather[0].description;
      const humidity = main.humidity;
      const windSpeed = wind.speed;

      weatherInfo.innerHTML = `
        <h2>${city}</h2>
        <p>${temperature}°C</p>
        <p>${description}</p>
        <p>Humidity: ${humidity}%</p>
        <p>Wind Speed: ${windSpeed} m/s</p>
      `;
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Event listener for the search button
searchButton.addEventListener("click", () => {
  const city = cityInput.value.trim();
  if (city) {
    getWeather(city);
  } else {
    weatherInfo.innerHTML = `<p>Please enter a city name.</p>`;
  }
});
