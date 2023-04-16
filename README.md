# Eat Exact
Tailor Your Plate, Don't Waste & Wait!
Made for HackOWASP 5.0 hackathon by Team Buzzfix

## Table of Contents

- Table of Contents
  - [Description](#description)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Credits](#credits)

## Description
Our project is a web-based platform that aims to
reduce food waste and improve efficiency in the
hospitality industry. The platform allows customers
staying in hotels, PGs, or messes to select their meals
in advance, so that only necessary food is prepared
and served, reducing food waste, saving money and
resources, and improving the dining experience.

## Getting Started

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/Ekuspreet/Eat-Exac
   ```
2. Install the required packages
   ```sh
   pip install flask flask-sqlalchemy solana
   ```
3. Navigate to the project directory
4. Run the following command in the terminal to setup database:
   ```sh
   python src/setup_db.py
   ``` 
5. Run the following command in the terminal to start the server:
   ```sh
   python src/main.py
   ``` 
6. Open your web browser and navigate to http://localhost:5000

### Usage

For Providers:
- Go to the registeration page and create an account for your organisation
- You will get a organisation_id, which you can circulate to your customers
- The customers can try to login with their room number and name, which will cause a request to pop up on your dashboard which you can review and approve
- The dashboard will also display the order summary and details for your organisation

For consumers:
- Login with your provided organisation_id and room number and name
- You can edit your order throught he dashboard as required


## Credits
- Ekuspreet Singh (Frontend)
- Devesh Sharma (Backend)
