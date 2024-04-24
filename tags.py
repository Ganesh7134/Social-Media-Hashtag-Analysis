import streamlit as st
import boto3
import json
import uuid  # for generating unique tag_id
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings

warnings.filterwarnings("ignore")

container = st.container()
try:
    with container:
        @st.cache_data(ttl=60 * 60)
        def load_lottie_file(filepath : str):
            with open(filepath, "r") as f:
                gif = json.load(f)
            st_lottie(gif, speed=1, width=650, height=450)
                
        load_lottie_file("tags.json")
except:
    print("Don't raise exception")
# Streamlit app title
st.title("Social Media Hashtag Analysis")

# Text input for user to enter hashtags
hashtags_input = st.text_area("Enter hashtags separated by spaces:")

# Function to extract hashtags from the input text
def extract_hashtags(input_text):
    words = input_text.split()
    hashtags = [word.strip("#") for word in words if word.startswith("#")]
    return hashtags

# Function to invoke AWS Lambda function
def invoke_lambda_function(hashtags):
    try:
        # Create a Lambda client
        lambda_client = boto3.client('lambda', 
                                     region_name='ca-central-1',
                                     aws_access_key_id='YOUR_ACCESS_KEY_ID',
                                     aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')
                                    )

        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName='HashtagsLambda',
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps({"hashtags": hashtags})
        )

        # Check if the invocation was successful
        if response['StatusCode'] == 200:
            return True
        else:
            st.error(f"Failed to invoke Lambda function. Status code: {response['StatusCode']}")
            return False
    except Exception as e:
        st.error(f"An error occurred while invoking the Lambda function: {str(e)}")
        return False

# Function to store hashtags in DynamoDB
def store_hashtags_in_dynamodb(hashtags):
    try:
        # Create a DynamoDB client
        dynamodb = boto3.resource('dynamodb',
                                  region_name='ca-central-1',
                                  aws_access_key_id='YOUR_ACCESS_KEY_ID',
                                  aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')
                                  )
        table = dynamodb.Table('tag_table')

        # Store each hashtag in DynamoDB
        for hashtag in hashtags:
            # Generate a unique tag_id
            tag_id = str(uuid.uuid4())
            # Put item into DynamoDB table
            table.put_item(Item={'tag_id': tag_id,'Hashtag': hashtag})
        
        return True
    except Exception as e:
        st.error(f"An error occurred while storing hashtags in DynamoDB: {str(e)}")
        return False

# Button to trigger the analysis
if st.button("Click here to analyze", key="my-btn", use_container_width=True):
    # Extract hashtags from the input text
    hashtags = extract_hashtags(hashtags_input)

    # Invoke Lambda function
    if invoke_lambda_function(hashtags):
        st.success("Lambda function invoked successfully.")
    
        # Store hashtags in DynamoDB
        if store_hashtags_in_dynamodb(hashtags):
            st.success("Hashtags stored successfully in DynamoDB.")
            st.balloons()
            # Function to fetch hashtags from DynamoDB
            def fetch_hashtags_from_dynamodb():
                try:
                    dynamodb = boto3.resource('dynamodb',
                                  region_name='ca-central-1',
                                  aws_access_key_id='YOUR_ACCESS_KEY_ID',
                                  aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')
                                  )

                    table = dynamodb.Table('tag_table')

                    response = table.scan()
                    items = response.get('Items', [])
                    # Extract hashtags and sort them in descending order
                    hashtags = sorted([item['Hashtag'] for item in items], reverse=True)

                    # Select the top 10 hashtags
                    top_10_hashtags = hashtags[:10]
                    return top_10_hashtags
                
                except Exception as e:
                    st.error(f"An error occurred while fetching hashtags from DynamoDB: {str(e)}")
                    return []
            
            fetched_hashtags = fetch_hashtags_from_dynamodb()
            if fetched_hashtags:
                st.header("Stored Hashtags:")
                for hashtag in fetched_hashtags:
                    st.write(f"- {hashtag}")
            
            # Function to generate word cloud
            def generate_word_cloud(hashtags):
                # Concatenate all hashtags into a single string
                text = ' '.join(hashtags)

                # Generate word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

                # Display word cloud
                fig, ax = plt.subplots(figsize=(10, 5))  # Create Matplotlib figure and axis
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title('Hashtag Word Cloud')
                st.pyplot(fig)  # Pass the figure object to st.pyplot()
                

            # Your Streamlit app code
            with st.expander("Word Cloud"):
                # Call the function to generate the word cloud
                generate_word_cloud(hashtags)
        else:
            st.error("Failed to store hashtags in DynamoDB.")
    else:
        st.error("Failed to invoke Lambda function.")

