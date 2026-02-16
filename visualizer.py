import matplotlib.pyplot as plt
import matplotlib

# Use a non-interactive backend to save files without opening windows
matplotlib.use('Agg') 

def create_plot(dataframe, title="Data Visualization"):
    """
    Generates a graph from the data and saves it as 'plot.png'.
    """
    plt.figure(figsize=(10, 6))
    
    # Simple logic: Plot the first two columns (X and Y axis)
    if len(dataframe.columns) >= 2:
        x_col = dataframe.columns[0]
        y_col = dataframe.columns[1]
        
        plt.bar(dataframe[x_col], dataframe[y_col], color='skyblue')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = "plot.png"
        plt.savefig(filename)
        plt.close()
        return filename
    else:
        return None