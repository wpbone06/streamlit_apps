import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import io

# Function to calculate rank changes between two selected days
def calculate_rank_changes(df, day1, day2):
    ranks_day1 = df[df['Date'] == day1].reset_index(drop=True)
    ranks_day2 = df[df['Date'] == day2].reset_index(drop=True)
    merged = pd.merge(ranks_day2, ranks_day1, on='name', how='left', suffixes=('_day2', '_day1'))
    rank_changes = merged['rank_day2'] - merged['rank_day1']
    player_names = merged['name']
    return rank_changes, player_names

# Function to plot rank changes for selected players
def plot_rank_changes(df, players):
    selected_data = df[df['name'].isin(players)]
    selected_data['Date'] = selected_data['Date'].str[5:]
    selected_data = selected_data.pivot(index='Date', columns='name', values='rank')
    selected_data.plot(marker='o')
#    ax = selected_data.plot(marker='o')
#    ax.set_xticklabels(pd.to_datetime(selected_data.index).strftime('%m-%d'))
    plt.xlabel('Date')
    plt.ylabel('rank')
    plt.title('Rank Changes for Selected Players')
    plt.legend()
    return plt

# Main function to run the Streamlit app
def main():
    st.title("Player Rank Change Analyzer")

    # Get the path to the player CSV file
    csv_file_path = "daily_consensus_ranks_2023-07-112023-08-03.csv"

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file_path)

    except Exception as e:
        st.error(f"Error: {e}")
        return

    # Display the DataFrame
    st.header("Player Rank Data")
    st.write(df)

    # Get unique days from the DataFrame
    unique_days = df['Date'].unique()

    # Select two days for rank comparison
    st.sidebar.header("Select Days")
    selected_days = st.sidebar.multiselect("Select two days", unique_days)

    if len(selected_days) == 2:
        day1, day2 = selected_days[0], selected_days[1]

        # Calculate rank changes and player names between selected days
        rank_changes, player_names = calculate_rank_changes(df, day1, day2)
        changes_df = pd.DataFrame({'Player': player_names, 'Rank Change': rank_changes})
        display_changes_df = changes_df.sort_values(by='Rank Change')

        # Reorder players and changes_df based on selected_players
        selected_players = st.sidebar.multiselect("Select players", sorted(df['name'].unique()))
        changes_df = changes_df[changes_df['Player'].isin(selected_players)]
        changes_df.sort_values('Player', inplace=True)
        player_names = changes_df['Player']
        rank_changes = changes_df['Rank Change']

        st.header("Rank Changes")
        st.write(display_changes_df)

        if selected_players:
            # Plot rank changes for selected players
            fig = plot_rank_changes(df, selected_players)
            st.pyplot(fig)

            # Download the plot as a PNG file
            st.sidebar.header('To download plot right click and select "Save Image As..."')

# Run the app
if __name__ == '__main__':
    main()

