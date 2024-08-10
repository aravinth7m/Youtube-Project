
# YouTube Data Harvesting & Warehousing

Welcome to the **YouTube Data Harvesting & Warehousing** project! This application allows you to collect, store, analyze, and visualize data from YouTube channels using the YouTube API. It's built using Python, Streamlit, and MySQL, providing a complete pipeline for YouTube data management.

## 🚀 Features

- **Data Collection**: Harvest YouTube channel data including video details, comments, and statistics.
- **Data Storage**: Store the collected data in a MySQL database for efficient querying and analysis.
- **SQL Analysis**: Perform SQL queries on the stored data to extract meaningful insights.
- **Data Visualization**: Visualize channel metrics, video performance, and other statistics directly in the Streamlit app.
- **User-Friendly Interface**: Intuitive and easy-to-use interface built with Streamlit.

## 📋 Project Structure

- **Main Application**: Streamlit app that provides an interactive interface for data collection, analysis, and visualization.
- **YouTube API Integration**: Python scripts to interact with the YouTube API and fetch channel data.
- **Database Management**: MySQL database setup to store and manage YouTube data.
- **Visualization**: Matplotlib and Streamlit used for creating visual representations of the data.

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- MySQL
- XAMPP (or any MySQL server)
- YouTube Data API v3 Key

### Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/youtube-data-harvesting.git
    cd youtube-data-harvesting
    ```

2. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup MySQL Database**:
   - Open XAMPP and start the MySQL server.
   - Create a database named `ytdatas`.

4. **Configure API Key**:
   - Replace the `api_key` in the code with your YouTube Data API v3 key.

5. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## 📊 Usage

1. **Home**: Overview of the project with a summary and introduction.
2. **Data Collection**: Enter a YouTube channel ID to collect and store data in the database.
3. **MySQL Database**: Execute predefined SQL queries to analyze the collected data.
4. **Analysis Using SQL**: Run custom SQL queries to explore the data further.
5. **Data Visualization**: Visualize YouTube channel and video statistics through various charts and graphs.

## 💡 Example Use Cases

- **Content Creators**: Analyze your channel's performance, viewer engagement, and popular videos.
- **Marketers**: Understand audience preferences and optimize content strategy.
- **Data Analysts**: Perform detailed analysis on YouTube data for insights and reporting.

## 📞 Contact

For any inquiries or support, please contact:

- **Aravinth M.**
- **Email**: [aravinth7m@gmail.com](mailto:aravinth7m@gmail.com)
- **LinkedIn**: [linkedin.com/in/aravinth7m](https://www.linkedin.com/in/aravinth7m)
