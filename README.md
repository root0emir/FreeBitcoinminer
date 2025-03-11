# FreeBitcoinminer

This tool is a Python application developed for Bitcoin mining. It performs Bitcoin mining based on user-defined parameters and reports the results to the user.

## Features

- **Subscription Process:** Used to listen for new blocks on the network and subscribe to mining operations.  
- **Mining Operations:** Performs Bitcoin mining according to specified parameters and solves blocks.  
- **Set Wallet Address:** Allows the user to configure their Bitcoin wallet address.  
- **Update Context Settings:** Updates the necessary settings for mining operations.  

## Requirements

This tool depends on the following Python libraries:

- binascii  
- hashlib  
- random  
- socket  
- requests  
- threading  
- time  
- json  
- colorama  
- signal  

To install the required dependencies, use the following command:

```sh
pip install -r requirements.txt
```

## Usage

Follow these steps to run the tool:

1. Clone the repository:
    ```sh
    git clone https://github.com/root0emir/FreeBitcoinminer.git
    cd bitcoin-mining
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Start the program:
    ```sh
    python main.py
    ```

Once the program starts, you will encounter the following menu options:

1. **Update Context Settings:** Updates the necessary settings for mining operations.  
2. **Set Wallet Address:** Allows you to set your Bitcoin wallet address.  
3. **Start Mining:** Starts the mining process.  
4. **Exit:** Exits the program.  

## License

This project is licensed under the MIT license. For more details, see the `LICENSE` file.

## Developer

This tool was developed by root0emir.
