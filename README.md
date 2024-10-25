# Viettel Can Tho - Sentiment Analysis and Data Analysis Project

This repository contains the work and models developed during my internship at Viettel Can Tho, focusing on analyzing customer feedback and optimizing data-based marketing strategies. The primary goal is to evaluate customer sentiments and identify insights to support strategic business improvements.

## Project Overview

During this project, I implemented various tasks, including data collection, preprocessing, feature extraction, and model building. Key components include:
1. **Data Collection and Preprocessing**: Collecting customer feedback from Google Maps reviews about Viettel Can Tho using web scraping techniques with Selenium and BeautifulSoup.
2. **Feature Engineering and Model Building**:
   - Text feature extraction using TF-IDF for analysis.
   - Addressing imbalanced data with the SMOTE technique.
   - Developing classification models: Multinomial Naive Bayes, Logistic Regression, and Random Forest.
3. **Evaluation and Analysis**: Analyzing model performance to assess the effectiveness of sentiment classification and providing insights for strategic recommendations.

## Files and Structure

- `data_collection/`: Scripts and tools for web scraping customer feedback.
- `data_preprocessing/`: Includes data cleaning and preprocessing workflows.
- `feature_engineering/`: Scripts for TF-IDF and SMOTE application.
- `models/`: Code for training classification models and evaluating performance.
- `visualizations/`: Data visualization tools using Power BI for displaying analytical insights.

## Requirements

- **Python 3.8+**
- **Libraries**: Install the necessary packages using `pip install -r requirements.txt`, including:
  - `Selenium` and `BeautifulSoup` for data collection
  - `Scikit-learn` for machine learning models
  - `Imbalanced-learn` for SMOTE implementation
  - `Pandas`, `Numpy` for data manipulation

## Usage

1. Clone the repository.
2. Run `data_collection/collect_reviews.py` to scrape Google Maps reviews.
3. Execute the scripts in `data_preprocessing/` to prepare the data for analysis.
4. Use `feature_engineering/tfidf_smote.py` for feature extraction.
5. Train models with scripts in `models/`.
6. View analytical results and visualizations in `visualizations/` with Power BI.

## Results and Recommendations

This project offers actionable insights into customer sentiment at Viettel Can Tho and identifies segments for potential marketing improvements based on behavioral data. Recommendations include targeted marketing strategies and service optimization based on identified customer needs.
