# File: app.py

import streamlit as st
from streamlit_searchbox import st_searchbox
from matplotlib.colors import to_rgba, rgb_to_hsv
import matplotlib.colors as mcolors
from visualize.chart import FlexibleSentimentAnalyzer, load_json_data
import matplotlib.pyplot as plt
import time
import random
from suggesions.phones import products

# Title of the app
st.title("Analysis of Smartphone Product Reviews on E-commerce Platforms")

# Suggestions list
suggestions = products

def show_progress_bar(x = 8, y = 10):
    gif_placeholder = st.empty()
    text_placeholder = st.empty()
    
    text_placeholder.markdown("<h3 style='text-align: center;'>Wait, I go get the data for you...</h3>", unsafe_allow_html=True)
    # Load and display the GIF with a smaller size and center it
    gif_html = '''
    <div style="display: flex; justify-content: center;">
        <iframe src="https://giphy.com/embed/Be4oArYyrPb1vY1hML" width="200" height="200" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    </div>
    '''
    gif_placeholder.markdown(gif_html, unsafe_allow_html=True)
    
    # Random duration between 8 and 10 seconds
    duration = random.uniform(x, y)
    
    # Sleep for the duration
    time.sleep(duration)
    
    # Remove the GIF and text after the duration
    gif_placeholder.empty()
    text_placeholder.empty()
def show_prediction_progress_bar():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    duration = random.uniform(6, 8)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        elapsed_time = time.time() - start_time
        progress = min(1.0, elapsed_time / duration)
        progress_bar.progress(progress)
        status_text.text("Prediction in progress...")
        time.sleep(0.1)
    
    progress_bar.empty()
    status_text.empty()
def search_function(query):
    # Return items that contain the query (case-insensitive)
    return [item for item in suggestions if query.lower() in item.lower()]

# Define a callback function to process the selected suggestion
def analyze_product(product):
    if "iphone 15 plus" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        visualize_sentiment_analysis_streamlit(data_path='visualize/data/iphone_reviews/iPhone_15_Plus_reviews.json') 
        return f"Analyzing reviews for: {product}"
    elif "iphone 15 pro max" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        visualize_sentiment_analysis_streamlit(data_path='visualize/data/iphone_reviews/iPhone_15_Pro_Max_reviews.json')
        return f"Analyzing reviews for: {product}"
    elif "iphone 15 pro" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        visualize_sentiment_analysis_streamlit(data_path='visualize/data/iphone_reviews/iPhone_15_Pro_reviews.json')
        return f"Analyzing reviews for: {product}"
    elif "iphone 15" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        visualize_sentiment_analysis_streamlit(data_path='visualize/data/iphone_reviews/iPhone_15_reviews.json')
        return f"Analyzing reviews for: {product}"
    elif "iphone 16" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        name = random.choice(["_Pro", "_Pro_Max", "_Plus", ""])
        visualize_sentiment_analysis_streamlit(data_path=f'visualize/data/iphone_reviews/iPhone_16{name}_reviews.json')
        return f"Analyzing reviews for: {product}"
    elif "samsung" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        ss = random.choice(["S24", "S24_Ultra", "S24+", "Z_Flip5", "Z_Fold5"])
        visualize_sentiment_analysis_streamlit(data_path=f'visualize/data/samsung_reviews/Samsung_Galaxy_{ss}_reviews.json')
        
        return f"Analyzing reviews for: {product}"
    elif "xiaomi" in product.lower() or "oppo" in product.lower() or "oneplus" in product.lower():
        # Create a placeholder for the chart
        show_progress_bar(x=3, y=4)
        # Generate the chart
        show_prediction_progress_bar()
        visualize_sentiment_analysis_streamlit()
        
        return f"Analyzing reviews for: {product}"
    else:
        show_progress_bar(x=3, y=4)
        # Display the text on top of the image, make it bigger, and change the color to red
        st.markdown("<h2 style='text-align: center; color: red;'>No products found or no reviews to analyze</h2>", unsafe_allow_html=True)
        # Display the image with a smaller size and center it
        st.image('animation/no-data.jpg', width=300, use_container_width=False)
        return "No data for analysis."

# Searchbox widget
selected_product = st_searchbox(
    search_function=search_function,  # Pass the search function
    label="Search for a smartphone",
    placeholder="Type to search..."
)

def visualize_sentiment_analysis_streamlit(data_path=None):
    """
    Visualize sentiment analysis results in a Streamlit app using matplotlib
    """
    # Create analyzer and get results
    analyzer = FlexibleSentimentAnalyzer()
    if data_path is not None:
        results = load_json_data(data_path)
    else:
        results = analyzer.analyze_comments()
    
    # Extract aspect summaries
    aspect_summaries = results['aspect_summaries']

    # Create a Streamlit container for visualizations
    st.title("Sentiment Analysis Visualization")
    
    # Create columns for the top row charts
    col1, col2 = st.columns(2)
    
    # Sentiment Distribution Pie Chart
    with col1:
        st.subheader("Overall Sentiment")
        sentiment_data = results['overall_summary']
        sentiment_labels = list(sentiment_data.keys())
        sentiment_values = list(sentiment_data.values())
        sentiment_colors = ['#4CAF50', '#F44336', '#2196F3']  # Green, Red, Blue
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sentiment_values, labels=sentiment_labels, colors=sentiment_colors, autopct='%1.1f%%')
        ax1.set_title('Overall Sentiment Distribution')
        st.pyplot(fig1)
    
    # Aspect Mentions Pie Chart
    with col2:
        st.subheader("Aspect Mentions")
        aspect_data = results['aspect_summaries']
        aspect_labels = list(aspect_data.keys())
        aspect_values = [data['total_mentions'] for data in aspect_data.values()]
        aspect_colors = ['#F707DC', '#36A2EB', '#FFCE56', '#4BC0C0', 
                         '#9966FF', '#FF9F40', '#E7E9ED', '#FF6384']
        
        fig2, ax2 = plt.subplots()
        ax2.pie(aspect_values, labels=aspect_labels, colors=aspect_colors[:len(aspect_labels)], autopct='%1.1f%%')
        ax2.set_title('Aspect Mentions Distribution')
        st.pyplot(fig2)
    
    # Create a column for the bottom row chart
    col3 = st.columns(1)[0]
    
    # Aspect Sentiment Polarity Distribution Pie Chart
    with col3:
        st.subheader("Aspect Sentiment Polarity")
        labels = []
        sizes = []
        colors = []
        color_palette = list(mcolors.CSS4_COLORS.values())
        color_cycle = len(color_palette)
        
        for i, (aspect, summary) in enumerate(aspect_summaries.items()):
            for sentiment, count in summary.items():
                if sentiment in ['Positive', 'Negative', 'Neutral'] and count > 0:
                    labels.append(f"{aspect}#{sentiment}")
                    sizes.append(count)
                    colors.append(color_palette[len(colors) % color_cycle])
        
        fig3, ax3 = plt.subplots()
        wedges, texts, autotexts = ax3.pie(
            sizes,
            colors=colors,
            autopct=lambda p: f'{p:.1f}%' if p >= 1 else '',
            startangle=90,
            pctdistance=0.85,
            labeldistance=1.1,
            textprops=dict(color="black")
        )
        
        for autotext, wedge in zip(autotexts, wedges):
            facecolor = wedge.get_facecolor()[:3]
            brightness = rgb_to_hsv(facecolor)[2]
            if brightness < 0.5:
                autotext.set_color('white')
            else:
                autotext.set_color('black')
        
        ax3.legend(
            labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10, title="Aspect#Sentiment"
        )
        ax3.set_title('Aspect Sentiment Polarity Distribution')
        st.pyplot(fig3)


# Analyze button
if st.button("Analyze"):
    result = analyze_product(selected_product)
    st.success(result)
