"""
Emoji visualization utilities for matplotlib plots.

This module provides functions to download emoji images and use them as 
axis labels in matplotlib plots. Perfect for creating engaging data 
visualizations with emoji elements!

Author: EDS 217 Course Materials
"""

import matplotlib.pyplot as plt
import requests
from PIL import Image
import io
import numpy as np
import matplotlib.offsetbox as ob

def get_emoji_image(emoji, transparent_bg=True):
    """
    Download an emoji image from online sources and return as numpy array.
    
    This function fetches emoji images from Twitter's Twemoji or Google's 
    Noto emoji collections. It automatically handles transparency and 
    provides fallback options if the emoji isn't found.
    
    Parameters
    ----------
    emoji : str
        A single emoji character (e.g., "😀", "🔥", "👍")
    transparent_bg : bool, default True
        If True, makes the background transparent. If False, keeps 
        the original background (usually white).
        
    Returns
    -------
    numpy.ndarray
        Image array with shape (72, 72, 4) for RGBA or (72, 72, 3) for RGB.
        
    Examples
    --------
    Get a fire emoji image:
    >>> img_array = get_emoji_image("🔥")
    >>> print(f"Image shape: {img_array.shape}")
    Image shape: (72, 72, 4)
    
    Get an emoji without transparency:
    >>> img_array = get_emoji_image("😀", transparent_bg=False)
    >>> print(f"Image shape: {img_array.shape}")
    Image shape: (72, 72, 3)
    """
    # Convert emoji to Unicode codepoint(s)
    # Handle multi-character emojis (e.g., emoji + variation selector)
    codepoints = []
    for char in emoji:
        codepoints.append(hex(ord(char))[2:].lower())
    
    # Join with underscores for multi-character emojis
    codepoint = "_".join(codepoints)
    
    # Try multiple emoji sources
    # Look for google emojis first; twitter emojis are 🤮
    urls = [
        f"https://github.com/googlefonts/noto-emoji/raw/main/png/72/emoji_u{codepoint}.png",
        f"https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/{codepoint}.png"
    ]
    
    # If multi-character, also try just the first character (base emoji)
    if len(codepoints) > 1:
        base_codepoint = codepoints[0]
        urls.extend([
            f"https://github.com/googlefonts/noto-emoji/raw/main/png/72/emoji_u{base_codepoint}.png",
            f"https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/{base_codepoint}.png"
        ])
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                
                # Keep transparency if it exists and requested
                if transparent_bg and img.mode in ('RGBA', 'LA'):
                    return np.array(img)  # Keep alpha channel
                elif transparent_bg:
                    # Convert to RGBA and make white pixels transparent
                    img = img.convert('RGBA')
                    data = np.array(img)
                    
                    # Make white/light pixels transparent
                    # Define what counts as "background" (light colors)
                    light_threshold = 240
                    mask = (data[:, :, 0] > light_threshold) & \
                           (data[:, :, 1] > light_threshold) & \
                           (data[:, :, 2] > light_threshold)
                    data[mask, 3] = 0  # Set alpha to 0 (transparent)
                    
                    return data
                else:
                    # No transparency requested
                    return np.array(img.convert('RGB'))
        except:
            continue
    
    # Fallback: create a colored square
    if transparent_bg:
        img = Image.new('RGBA', (72, 72), color=(200, 200, 200, 255))
    else:
        img = Image.new('RGB', (72, 72), color=(200, 200, 200))
    return np.array(img)

def display_emoji_image(emoji):
    """
    Display a single emoji image in its own matplotlib figure.
    
    This is a helper function to quickly preview how an emoji will look
    when downloaded and processed. Useful for testing before adding 
    emojis to your main plots.
    
    Parameters
    ----------
    emoji : str
        A single emoji character to display (e.g., "🎉", "📊", "🐍")
        
    Returns
    -------
    None
        Displays the image and prints shape information.
        
    Examples
    --------
    Preview a single emoji:
    >>> display_emoji_image("🐍")
    Getting image for: 🐍
    Image shape: (72, 72, 4)
    Image type: <class 'numpy.ndarray'>
    
    Test multiple emojis:
    >>> for emoji in ["😀", "😂", "🔥"]:
    ...     display_emoji_image(emoji)
    """
    print(f"Getting image for: {emoji}")
    
    # Get the emoji image
    img_array = get_emoji_image(emoji)
    
    # Display it
    plt.figure(figsize=(0.5, 0.5))
    plt.imshow(img_array)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    print(f"Image shape: {img_array.shape}")
    print(f"Image type: {type(img_array)}")
    
def emoji_labels(ax, ticks, emojis, zoom=0.8, y_offset=-18):
    """
    Replace x-axis tick labels with emoji images.
    
    This function removes the default text labels from the x-axis and 
    replaces them with emoji images positioned at the specified tick 
    locations. Perfect for creating engaging categorical plots!
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axis object to modify.
    ticks : array-like
        Tick positions where emojis should be placed (e.g., [0, 1, 2, 3]).
        Should match the x-coordinates of your data.
    emojis : list of str
        Emoji characters to use as labels. Must be the same length as ticks.
        Each element should be a single emoji (e.g., ["😀", "😂", "🔥"]).
    zoom : float, default 0.8
        Scaling factor for emoji size. Larger values = bigger emojis.
        Try values between 0.5 and 1.2 for best results.
    y_offset : int, default -18
        Vertical offset in points to position emojis below the axis line.
        More negative values move emojis further down.
        
    Returns
    -------
    None
        Modifies the provided axis object in-place.
        
    Examples
    --------
    Basic bar chart with emoji labels:
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> 
    >>> # Sample data
    >>> emojis = ["😀", "😂", "😍", "🔥", "👍"]
    >>> values = [10, 25, 15, 30, 20]
    >>> x = np.arange(len(values))
    >>> 
    >>> # Create plot
    >>> fig, ax = plt.subplots(figsize=(6, 4))
    >>> ax.bar(x, values)
    >>> 
    >>> # Add emoji labels
    >>> emoji_labels(ax, ticks=x, emojis=emojis)
    >>> 
    >>> ax.set_ylabel("Usage count")
    >>> ax.set_title("Emoji Usage")
    >>> plt.show()
    
    Line plot with weather emojis:
    >>> days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    >>> temps = [22, 25, 18, 30, 28]
    >>> weather_emojis = ["☀️", "🌤️", "🌧️", "🔥", "☀️"]
    >>> x = np.arange(len(days))
    >>> 
    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, temps, marker='o')
    >>> emoji_labels(ax, ticks=x, emojis=weather_emojis, zoom=1.0)
    >>> ax.set_ylabel("Temperature (°C)")
    >>> plt.show()
    
    Notes
    -----
    - Make sure your figure has enough bottom margin for the emojis:
      use plt.subplots_adjust(bottom=0.2) or fig.tight_layout() if needed
    - Emojis are downloaded from online sources, so internet connection required
    - If an emoji fails to download, a gray square placeholder is used
    """
    # Clear default text labels
    ax.set_xticks(ticks)
    ax.set_xticklabels([])
    
    # Drop emoji images at each tick
    for xi, e in zip(ticks, emojis):
        img = get_emoji_image(e, transparent_bg=True)
        oi = ob.OffsetImage(img, zoom=zoom)
        ab = ob.AnnotationBbox(
            oi,
            (xi, 0),
            xybox=(0, y_offset),
            frameon=False,
            boxcoords="offset points",
            pad=0
        )
        ax.add_artist(ab)


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

def example_basic_bar_chart():
    """
    Complete example showing how to create a bar chart with emoji labels.
    
    This example demonstrates the most common use case: replacing categorical
    x-axis labels with emoji images.
    """
    import numpy as np
    
    print("Creating basic bar chart with emoji labels...")
    
    # --- Example usage ---
    emojis = ["😀", "😂", "😍", "🔥", "👍"]
    values = [10, 25, 15, 30, 20]
    x = np.arange(len(values))

    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    ax.bar(x, values)

    # One-liner: set ticks, then replace with emoji labels
    emoji_labels(ax, ticks=x, emojis=emojis)

    ax.set_ylabel("Usage count")
    ax.set_title("Emoji Usage")
    # fig.subplots_adjust(bottom=0.25)  # make room for emojis
    plt.show()
    
    print("Bar chart complete!")


def example_weather_data():
    """
    Example showing emoji labels with time series weather data.
    """
    import numpy as np
    
    print("Creating weather chart with emoji labels...")
    
    # Weather data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    temps = [22, 25, 18, 30, 28, 24, 26]
    weather_emojis = ["☀️", "🌤️", "🌧️", "🔥", "☀️", "⛅", "🌞"]
    
    x = np.arange(len(days))
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, temps, marker='o', linewidth=2, markersize=8)
    
    # Add emoji labels
    emoji_labels(ax, ticks=x, emojis=weather_emojis, zoom=1.0)
    
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Weekly Weather Forecast")
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("Weather chart complete!")


if __name__ == "__main__":
    print("Running emoji visualization examples...")
    print("\n" + "="*50)
    print("Example 1: Basic Bar Chart")
    print("="*50)
    example_basic_bar_chart()
    
    print("\n" + "="*50)
    print("Example 2: Weather Data")
    print("="*50)
    example_weather_data()
    
    print("\n" + "="*50)
    print("Example 3: Single Emoji Preview")
    print("="*50)
    display_emoji_image("🐍")
    display_emoji_image("📊")
    
    print("\nAll examples completed! 🎉")