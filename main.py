import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


# scraping hotel informations from the website
def scrape_hotels(city, checkin_date, checkout_date):
    try:
        url = (f'https://www.booking.com/searchresults.html?ss={city}&checkin={checkin_date}&checkout={checkout_date}&g'
               f'roup_adults=2&no_rooms=1&group_children=0')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 51.'
                          '0.2704.64 Safari / 537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

        # http request and fetching hotel infos
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        # hotels list
        hotel_data = []

        for hotel in hotels:
            name_element = hotel.find('div', {'data-testid': 'title'})
            name = name_element.text.strip() if name_element else 'NOT GIVEN'

            address_element = hotel.find('span', {'data-testid': 'address'})
            address = address_element.text.strip() if address_element else 'NOT GIVEN'

            distance_element = hotel.find('span', {'data-testid': 'distance'})
            distance = distance_element.text.strip() if distance_element else 'NOT GIVEN'

            rating_element = hotel.find('div', {'data-testid': 'review-score'})
            rating = rating_element.text.strip() if rating_element else 'NOT GIVEN'

            price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
            price = price_element.text.strip() if price_element else 'NOT GIVEN'

            if selected_option.get() == "Euro" and re.search(r'\bTL\b', price):
                price_value_match = re.search(r'[\d,]+', price)
                if price_value_match:
                    price_value = price_value_match.group().replace(",", "")
                    try:
                        price_value = int(price_value)
                        price = f"€ {price_value / 30:.2f}"
                    except ValueError:
                        pass

            # hotel informations are stored in a dictionary
            hotel_data.append({'Name': name,
                               'Address': address,
                               'Distance': distance,
                               'Rating': rating,
                               'Price': price})

        return hotel_data[:5]  # top 5 hotels

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def select_checkin_date():
    def set_checkin_date():
        try:
            checkin_entry.delete(0, tk.END)
            checkin_entry.insert(0, cal.selection_get().strftime('%d-%m-%Y'))
        finally:
            top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='d-m-Y')
    cal.pack()
    ok_button = tk.Button(top, text="OK", command=set_checkin_date)
    ok_button.pack()


def select_checkout_date():
    def set_checkout_date():
        try:
            checkout_entry.delete(0, tk.END)
            checkout_entry.insert(0, cal.selection_get().strftime('%d-%m-%Y'))
        finally:
            top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='d-m-Y')
    cal.pack()
    ok_button = tk.Button(top, text="OK", command=set_checkout_date)
    ok_button.pack()


def search_hotels():
    city = city_combobox.get()
    checkin_date_str = checkin_entry.get()
    checkout_date_str = checkout_entry.get()

    if not city or not checkin_date_str or not checkout_date_str:
        messagebox.showinfo("Info", "Please fill all fields.")
        return

    try:
        checkin_date = datetime.strptime(checkin_date_str, '%d-%m-%Y').date()
        checkout_date = datetime.strptime(checkout_date_str, '%d-%m-%Y').date()

        if checkin_date >= checkout_date:
            messagebox.showinfo("Error", "Check-out date should be later than check-in date.")
            return

        hotels = scrape_hotels(city, checkin_date, checkout_date)
        if hotels:
            hotel_infos(hotels)
        else:
            messagebox.showinfo("Info", "No hotels found.")

    except ValueError:
        error_window = tk.Toplevel(root)
        error_window.title("Error")
        error_label = ttk.Label(error_window, text="Invalid date format. Please use dd-mm-yyyy.")
        error_label.pack()
        ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack()


def hotel_infos(hotels):
    hotel_window = tk.Toplevel(root)
    hotel_window.title("Hotel Information")
    hotel_window.geometry("600x400")  # Set the size of the new window
    hotel_frame = ttk.Frame(hotel_window, padding="10")
    hotel_frame.grid(row=0, column=0, sticky="nsew")

    row_num = 0
    for idx, hotel in enumerate(hotels, start=1):
        hotel_label = ttk.Label(hotel_frame, text=f"Hotel {idx}:")
        hotel_label.grid(row=row_num, column=0, sticky="w", pady=(5, 0))
        row_num += 1
        for key, value in hotel.items():
            info_label = ttk.Label(hotel_frame, text=f"{key}: {value}")
            info_label.grid(row=row_num, column=0, sticky="w")
            row_num += 1
        row_num += 1  # Add extra space between hotels


root = tk.Tk()
root.title("Hotel Program")

program_frame = ttk.Frame(root, padding="20")
program_frame.grid(row=0, column=0)

searcher_label = ttk.Label(program_frame, text="Hotel Searcher")
searcher_label.grid(row=0, column=0, columnspan=3)

empty_label = ttk.Label(program_frame, text="")
empty_label.grid(row=1, column=0)  # empty row

city_label = ttk.Label(program_frame, text="Select City")
city_label.grid(row=2, column=0, sticky="w")

# cities list
cities = ['Rome', 'Paris', 'Amsterdam', 'London', 'Prague', 'Athens', 'Munich', 'Venice', 'Lisbon', 'Dublin']
city_combobox = ttk.Combobox(program_frame, values=cities)
city_combobox.grid(row=2, column=1, pady=5)

checkin_label = ttk.Label(program_frame, text="Check in Date")
checkin_label.grid(row=3, column=0, sticky="w")
checkin_entry = ttk.Entry(program_frame)
checkin_entry.grid(row=3, column=1, pady=3)
checkin_button = ttk.Button(program_frame, text="Select Date", command=select_checkin_date)
checkin_button.grid(row=3, column=2)

checkout_label = ttk.Label(program_frame, text="Check out Date")
checkout_label.grid(row=4, column=0, sticky="w")
checkout_entry = ttk.Entry(program_frame)
checkout_entry.grid(row=4, column=1, pady=3)
checkout_button = ttk.Button(program_frame, text="Select Date", command=select_checkout_date)
checkout_button.grid(row=4, column=2)

search_button = ttk.Button(program_frame, text="Search Hotels", command=search_hotels)
search_button.grid(row=5, column=0, columnspan=2, padx=30, pady=15)

option_frame = ttk.Frame(program_frame)
option_frame.grid(row=5, column=2, padx=30, pady=15)

selected_option = tk.StringVar(value="TL")

option_a_radio = ttk.Radiobutton(option_frame, text="TL", variable=selected_option, value="TL")
option_a_radio.grid(row=0, column=0, padx=5)
option_b_radio = ttk.Radiobutton(option_frame, text="Euro", variable=selected_option, value="Euro")
option_b_radio.grid(row=0, column=1, padx=5)

root.mainloop()
