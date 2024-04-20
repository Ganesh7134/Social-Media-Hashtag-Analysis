# Social Media Hashtag Analysis
This is a Streamlit web application for analyzing and storing social media hashtags using AWS Lambda and DynamoDB.

## Overview
The application allows users to input hashtags, which are then sent to an AWS Lambda function for analysis. The Lambda function processes the hashtags and stores them in a DynamoDB table. Finally, the top 10 hashtags stored in DynamoDB are displayed back to the user.

## Features
* Input area to enter hashtags separated by spaces.
* Clickable button to trigger the analysis and storage process.
* Visualization of stored hashtags using **Word cloud**.
* Error handling for AWS Lambda and DynamoDB interactions.

## Requirements
* Python 3.6+
* Streamlit
* boto3
* AWS account with configured Lambda and DynamoDB resources


## Conclusion

In summary, the Social Media Hashtag Analysis tool simplifies the process of analyzing and storing social media hashtags. Users can input hashtags easily and trigger the analysis with a click. The app then visualizes the top 10 hashtags, offering insights into trending topics. With robust error handling, it ensures a smooth user experience. This tool is ideal for anyone seeking to understand social media trends quickly and efficiently
