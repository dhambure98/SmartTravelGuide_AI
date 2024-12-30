# Personalized Travel Recommender  
**EEX6340 Artificial Intelligence Techniques & Agent Technology Mini Project**  

A web-based application that provides personalized travel recommendations based on user preferences, budget, and age. This project leverages Flask for the backend, React for the frontend, and the `Travel.csv` dataset to deliver customized suggestions.  

---

## Features  
- Personalized travel recommendations.  
- Filter destinations based on user preferences, budget, and age.  
- User-friendly interface with seamless interaction between the frontend and backend.  
- RESTful API implementation for efficient data handling.  

---

## Technologies Used  
### Backend  
- **Flask**: A lightweight WSGI web application framework for building the API.  
- **Pandas**: For data processing and filtering recommendations from the `Travel.csv` dataset.  
- **Flask-CORS**: To handle Cross-Origin Resource Sharing issues between the backend and frontend.  

### Frontend  
- **React**: For building a dynamic and responsive user interface.  
- **Fetch API**: To send POST and GET requests to the Flask backend.  

---

## Dataset  
The application uses `Travel.csv`, a dataset containing:  
- User demographics (age, preferences, budget).  
- Destination details (name, region, attractions, best season, popularity).  

---

## Setup and Installation  

### Prerequisites  
- Python 3.8+  
- Node.js and npm  
- React CLI  

### Backend Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/PersonalizedTravelRecommender.git
   cd PersonalizedTravelRecommender/backend
