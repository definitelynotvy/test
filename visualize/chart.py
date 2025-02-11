import random
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.colors import rgb_to_hsv

class FlexibleSentimentAnalyzer:
    def __init__(self, num_comments=None, aspects=None, sparsity_factor=0.2, incomplete_aspect_factor=0.15):
        """
        Initialize the sentiment analyzer with more nuanced simulation parameters
        
        :param num_comments: Number of comments to generate
        :param aspects: List of product aspects
        :param sparsity_factor: Probability of an aspect being completely skipped
        :param incomplete_aspect_factor: Probability of an aspect having incomplete sentiment data
        """
        # Randomly choose number of comments between 10 and 50
        self.num_comments = num_comments or random.randint(25, 45)
        self.aspects = aspects or [
            'SCREEN', 'CAMERA', 'BATTERY', 'PERFORMANCE', 'GENERAL',
            'STORAGE', 'DESIGN', 'PRICE', 'SERVICE&ACCESSORIES', 'FEATURES'
        ]
        
        # New parameters to control simulation complexity
        self.sparsity_factor = sparsity_factor  # Controls skipping of aspects
        self.incomplete_aspect_factor = incomplete_aspect_factor  # Controls incomplete sentiment data
    
    def generate_aspect_coverage(self):
        """
        Create a more nuanced aspect coverage model with sparsity
        """
        base_probabilities = {
            'CAMERA': random.uniform(0.4, 0.8),
            'BATTERY': random.uniform(0.1, 0.6),
            'PRICE': random.uniform(0.3, 0.6),
            'GENERAL': random.uniform(0.5, 0.8),
            'FEATURES': random.uniform(0.2, 0.6),
            'PERFORMANCE': random.uniform(0.3, 0.4),
            'SCREEN': random.uniform(0.1, 0.5),
            'DESIGN': random.uniform(0.05, 0.4),
            'STORAGE': random.uniform(0, 0.3),
            'SERVICE&ACCESSORIES': random.uniform(0, 0.2)
        }
        
        # Apply sparsity: some aspects might be completely skipped
        for aspect in base_probabilities:
            if random.random() < self.sparsity_factor:
                base_probabilities[aspect] = 0
        
        return base_probabilities
    
    def generate_sentiment(self, allow_missing=False):
        """
        Generate sentiment with more flexible options
        
        :param allow_missing: If True, can return None to simulate incomplete data
        """
        if allow_missing and random.random() < self.incomplete_aspect_factor:
            return None
        
        sentiments = ['Positive', 'Negative', 'Neutral']
        weights = [0.52, 0.2, 0.28]  # Slightly adjusted distribution
        return random.choices(sentiments, weights=weights)[0]
    
    def analyze_comments(self):
        """
        Simulate a flexible, realistic review analysis with edge cases
        """
        # Generate aspect coverage probabilities
        aspect_coverage = self.generate_aspect_coverage()
        
        # Initialize tracking with more flexible structure
        aspect_sentiments = {
            aspect: {
                'Positive': 0, 
                'Negative': 0, 
                'Neutral': 0, 
                'total_mentions': 0,
                'missing_sentiment': 0  # Track aspects with no sentiment
            }
            for aspect in self.aspects
        }
        
        overall_sentiments = []
        
        # Simulate comments
        for _ in range(self.num_comments):
            # Randomly select which aspects are mentioned
            mentioned_aspects = [
                aspect for aspect in self.aspects 
                if random.random() < aspect_coverage[aspect]
            ]
            
            # Ensure at least one aspect is mentioned (with reduced probability)
            if not mentioned_aspects and random.random() > 0.3:
                mentioned_aspects = [random.choice(self.aspects)]
            
            # Generate sentiment for mentioned aspects
            for aspect in mentioned_aspects:
                sentiment = self.generate_sentiment(allow_missing=True)
                
                # Track aspect-level sentiments
                if sentiment is None:
                    aspect_sentiments[aspect]['missing_sentiment'] += 1
                else:
                    aspect_sentiments[aspect][sentiment] += 1
                    overall_sentiments.append(sentiment)
                
                aspect_sentiments[aspect]['total_mentions'] += 1
        
        # Overall sentiment summary
        overall_summary = {
            sentiment: overall_sentiments.count(sentiment)
            for sentiment in ['Positive', 'Negative', 'Neutral']
        }
        
        # Compute aspect-level summaries
        aspect_summaries = {}
        for aspect, sentiments in aspect_sentiments.items():
            total_mentions = sentiments['total_mentions']
            
            # Only include aspects with mentions
            if total_mentions > 0:
                # Calculate percentages, handling potential division by zero
                def safe_percentage(count):
                    return round(count / total_mentions * 100, 2) if total_mentions > 0 else 0
                
                aspect_summaries[aspect] = {
                    'Positive': sentiments['Positive'],
                    'Negative': sentiments['Negative'],
                    'Neutral': sentiments['Neutral'],
                    'missing_sentiment': sentiments['missing_sentiment'],
                    'total_mentions': total_mentions,
                    'positive_percentage': safe_percentage(sentiments['Positive']),
                    'negative_percentage': safe_percentage(sentiments['Negative']),
                    'neutral_percentage': safe_percentage(sentiments['Neutral']),
                    'missing_sentiment_percentage': safe_percentage(sentiments['missing_sentiment'])
                }
        
        return {
            'total_comments': self.num_comments,
            'overall_summary': overall_summary,
            'aspect_summaries': aspect_summaries
        }



def load_json_data(path):
    import json
    
    with open(path, 'r') as file:
        data = json.load(file)
    return data

# Usage example:
# json_data = load_json_data()

def visualize_sentiment_analysis():
    """
    Visualize sentiment analysis results using matplotlib
    """
    # Create analyzer and get results
    # analyzer = FlexibleSentimentAnalyzer()
    # results = analyzer.analyze_comments()
    # print(results)
    results = load_json_data('visualize/iphone16.json')
    # Extract aspect summaries
    aspect_summaries = results['aspect_summaries']

    # Set up the plotting
    plt.figure(figsize=(20, 8))
    
    # Sentiment Distribution Pie Chart
    plt.subplot(1, 3, 1)
    sentiment_data = results['overall_summary']
    sentiment_labels = list(sentiment_data.keys())
    sentiment_values = list(sentiment_data.values())
    sentiment_colors = ['#4CAF50', '#F44336', '#2196F3']  # Green, Red, Blue
    
    plt.pie(sentiment_values, labels=sentiment_labels, colors=sentiment_colors, autopct='%1.1f%%')
    plt.title('Overall Sentiment Distribution')
    
    # Aspect Mentions Pie Chart
    plt.subplot(1, 3, 2)
    aspect_data = results['aspect_summaries']
    aspect_labels = list(aspect_data.keys())
    aspect_values = [data['total_mentions'] for data in aspect_data.values()]
    aspect_colors = ['#F707DC', '#36A2EB', '#FFCE56', '#4BC0C0', 
                     '#9966FF', '#FF9F40', '#E7E9ED', '#FF6384']
    
    plt.pie(aspect_values, labels=aspect_labels, colors=aspect_colors[:len(aspect_labels)], autopct='%1.1f%%')
    plt.title('Aspect Mentions Distribution')
    
    plt.subplot(1, 3, 3)
    # Prepare data for pie chart
    labels = []
    sizes = []
    colors = []
    
    # Use a large, diverse color palette
    color_palette = list(mcolors.CSS4_COLORS.values())
    color_cycle = len(color_palette)
    
    for i, (aspect, summary) in enumerate(aspect_summaries.items()):
        for sentiment, count in summary.items():
            if sentiment in ['Positive', 'Negative', 'Neutral'] and count > 0:
                labels.append(f"{aspect}#{sentiment}")
                sizes.append(count)
                colors.append(color_palette[len(colors) % color_cycle])  # Assign unique color
    
    # Plotting the pie chart
    wedges, texts, autotexts = plt.pie(
        sizes,
        colors=colors,
        autopct=lambda p: f'{p:.1f}%' if p >= 1 else '',
        startangle=90,
        pctdistance=0.85,
        labeldistance=1.1,
        textprops=dict(color="black")  # Default text color is black
    )
    
    # Adjust text color for slices with dark backgrounds
    for autotext, wedge in zip(autotexts, wedges):
        # Convert wedge color to HSV to check brightness
        facecolor = wedge.get_facecolor()[:3]  # Get RGB part
        brightness = rgb_to_hsv(facecolor)[2]  # HSV brightness (value)
        
        if brightness < 0.5:  # Dark background
            autotext.set_color('white')
        else:
            autotext.set_color('black')
    
    # Add legend
    plt.legend(
        labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10, title="Aspect#Sentiment"
    )
    plt.title('Aspect Sentiment Polarity Distribution')
    
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()

def visualize():
    """
    Visualize sentiment analysis with:
    - Numbers in black by default.
    - Numbers in white for dark backgrounds.
    - Small slices (<1%) displayed outside the chart.
    """
    # Create analyzer and get results
    analyzer = FlexibleSentimentAnalyzer()
    results = analyzer.analyze_comments()
    
    # Extract data
    aspect_summaries = results['aspect_summaries']
    
    # Prepare data for pie chart
    labels = []
    sizes = []
    colors = []
    
    # Use a large, diverse color palette
    color_palette = list(mcolors.CSS4_COLORS.values())
    color_cycle = len(color_palette)
    
    for i, (aspect, summary) in enumerate(aspect_summaries.items()):
        for sentiment, count in summary.items():
            if sentiment in ['Positive', 'Negative', 'Neutral'] and count > 0:
                labels.append(f"{aspect}#{sentiment}")
                sizes.append(count)
                colors.append(color_palette[len(colors) % color_cycle])  # Assign unique color
    
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(
        sizes,
        colors=colors,
        autopct=lambda p: f'{p:.1f}%' if p >= 1 else '',
        startangle=90,
        pctdistance=0.85,
        labeldistance=1.1,
        textprops=dict(color="black")  # Default text color is black
    )
    
    # Adjust text color for slices with dark backgrounds
    for autotext, wedge in zip(autotexts, wedges):
        # Convert wedge color to HSV to check brightness
        facecolor = wedge.get_facecolor()[:3]  # Get RGB part
        brightness = rgb_to_hsv(facecolor)[2]  # HSV brightness (value)
        
        if brightness < 0.5:  # Dark background
            autotext.set_color('white')
        else:
            autotext.set_color('black')
    
    # Add legend
    ax.legend(
        labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10, title="Aspect#Sentiment"
    )
    
    # Title and formatting
    ax.set_title('Aspect Sentiment Polarity Distribution', fontsize=14)
    plt.tight_layout()
    plt.show()

# Run the visualization
if __name__ == '__main__':
    visualize_sentiment_analysis()

