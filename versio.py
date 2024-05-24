import re
import time
from telethon.sync import TelegramClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os

api_id = 22700884
api_hash = '00cbbf88cbe55b5f46ca22eb155f6343'

# Configure Selenium WebDriver
os.environ['PATH'] += ':/usr/local/bin'  # Add geckodriver path to the system PATH
options = Options()
options.headless = False  # Set to True if you want to run Firefox in headless mode

accounts = [
    {"username": "william_zilyy_wily1212", "password": "avotra"},
    {"username": "urki_jelk12", "password": "avotra"}
]
current_account_index = 0

# Dictionnaire pour stocker les derniers liens traités pour chaque compte
last_link_per_account = {}

def handle_notifications(driver):
    try:
        notification_button = driver.find_element(By.CLASS_NAME, "_a9_1")
        notification_button.click()
        print("Notification popup closed.")
    except Exception as e:
        print(f"No notification popup found: {str(e)}")

    try:
        not_now_button = driver.find_element(By.XPATH, "//button[text()='Not Now']")
        not_now_button.click()
        print("Second popup closed.")
    except Exception as e:
        print(f"No second notification popup found: {str(e)}")

def Cookies1(driver):
    try:
        driver.find_element(By.CLASS_NAME, "_ac8f").click()
        print("Cookies popup closed")
    except:
        print("Cookies popup not found")

def login(driver, username, password):
    driver.get("https://www.instagram.com")
    try:
        cookies = False
        while not cookies:
            try:
                if driver.find_element(By.NAME, "username"):
                    driver.find_element(By.NAME, "username").send_keys(username)
                    driver.find_element(By.NAME, "password").send_keys(password)
                    cookies = True

                    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    login_button.click()

                    time.sleep(10)  # Wait for the page to load

                    try:
                        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button').click()
                        time.sleep(10)
                        driver.find_element(By.CLASS_NAME, "_a9_1").click()
                        print("Secondary popup handled")
                    except:
                        pass

                    connect = False
                    while not connect:
                        try:
                            if driver.find_element(By.CLASS_NAME, "xuxw1ft"):
                                print(f"Connected with account: {username}")
                                return True
                        except:
                            pass
            except:
                pass
    except Exception as e:
        print(f"Failed to connect with account: {username}, Error: {str(e)}")
    return False

def logout(driver):
    try:
        driver.get("https://www.instagram.com")
        profile_icon = driver.find_element(By.CLASS_NAME, "xzzcqpx")
        profile_icon.click()
        time.sleep(2)
        logout_button = driver.find_element(By.CLASS_NAME, "xuxw1ft")
        logout_button.click()
        time.sleep(2)
        print("Logged out successfully.")
    except Exception as e:
        print(f"Error during logout: {str(e)}")

def restart_browser(driver=None):
    if driver is not None:
        driver.quit()
    return webdriver.Firefox(options=options)

def Follow(driver, url):
    driver.get(url)
    handle_notifications(driver)
    try:
        time.sleep(5)  # Adjust the wait time according to your internet speed
        
        follow_button = driver.find_element(By.CLASS_NAME, "_acan")
        
        # Verify if the profile is already followed
        svg = follow_button.find_element(By.TAG_NAME, "svg")
        if svg.get_attribute("aria-label") != "Following":
            follow_button.click()
            handle_notifications(driver)
            time.sleep(2)  # Wait for a short time to ensure the follow action is registered
            
            # Verify again to ensure the profile is followed
            svg = follow_button.find_element(By.TAG_NAME, "svg")
            if svg.get_attribute("aria-label") == "Following":
                print("Profile followed successfully!")
            else:
                print("Failed to follow the profile. Retrying...")
                follow_button.click()
                handle_notifications(driver)
                time.sleep(2)  # Wait for a short time to ensure the follow action is registered again
                svg = follow_button.find_element(By.TAG_NAME, "svg")
                if svg.get_attribute("aria-label") == "Following":
                    print("Profile followed successfully on retry!")
                else:
                    print("Failed to follow the profile after retry.")
        else:
            print("Profile was already followed.")
    except Exception as e:
        print(f"An error occurred during follow: {str(e)}")


def Like(driver, post_url):
    driver.get(post_url)
    handle_notifications(driver)
    try:
        time.sleep(5)  # Adjust the wait time according to your internet speed
        
        like_button = driver.find_element(By.CLASS_NAME, "xp7jhwk")
        
        # Verify if the post is already liked
        svg = like_button.find_element(By.TAG_NAME, "svg")
        if svg.get_attribute("aria-label") != "Unlike":
            like_button.click()
            handle_notifications(driver)
            time.sleep(2)  # Wait for a short time to ensure the like action is registered
            
            # Verify again to ensure the post is liked
            svg = like_button.find_element(By.TAG_NAME, "svg")
            if svg.get_attribute("aria-label") == "Unlike":
                print("Post liked successfully!")
            else:
                print("Failed to like the post. Retrying...")
                like_button.click()
                handle_notifications(driver)
                time.sleep(2)  # Wait for a short time to ensure the like action is registered again
                svg = like_button.find_element(By.TAG_NAME, "svg")
                if svg.get_attribute("aria-label") == "Unlike":
                    print("Post liked successfully on retry!")
                else:
                    print("Failed to like the post after retry.")
        else:
            print("Post was already liked.")
    except Exception as e:
        print(f"An error occurred during like: {str(e)}")


def extract_links(text):
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    links = list(set(links))
    cleaned_links = [link.strip('()[]') for link in links]
    return cleaned_links

def main():
    global current_account_index
    global last_link_per_account  # Declare the global variable to be used inside the function
    driver = webdriver.Firefox(options=options)
    handle_notifications(driver)
    
    with TelegramClient('name', api_id, api_hash) as client:
        client.send_message('https://t.me/SmmKingdomTasksBot', "📝Tasks📝")
        print("Bot launched and initial message sent.")
        
        while True:
            try:
                unread_messages = client.iter_messages('https://t.me/SmmKingdomTasksBot')
                print("ity ny message via telegram")
                print(unread_messages)
                print("*************************")
                for message in unread_messages:
                    handle_notifications(driver)
                    
                    current_account = accounts[current_account_index]
                    account_username = current_account["username"]
                    
                    if "Sorry, but there are no active tasks at the moment" in message.text:
                        current_account_index = (current_account_index + 1) % len(accounts)
                        current_account = accounts[current_account_index]
                        print(f"Switching account: {current_account['username']}")
                        
                        if current_account_index == 0:
                            print("Full round completed, waiting 20 seconds.")
                            time.sleep(20)
                        
                    else:
                        print(f"Processing with account: {account_username}")

                        if "Turn On Threads on your accounts" in message.text:
                            client.send_message('https://t.me/SmmKingdomTasksBot', "Instagram")
                            print(f"Sent 'Instagram' for account: {account_username}")
                        elif "Please give us your profile's username for tasks completing :" in message.text:
                            client.send_message('https://t.me/SmmKingdomTasksBot', account_username)
                            print(f"Sent username for account: {account_username}")
                        elif "Like the post below" in message.text:
                            links = extract_links(message.text)
                            if links:
                                link = links[0]
                                if last_link_per_account.get(account_username) != link:
                                    print(f"Extracted link for account {account_username}: {link}")
                                    if login(driver, current_account["username"], current_account["password"]):
                                        handle_notifications(driver)
                                        Like(driver, link)
                                        client.send_message('https://t.me/SmmKingdomTasksBot', "✅Completed")
                                        print(f"'Like' task completed for account {account_username}")
                                        last_link_per_account[account_username] = link  # Update the last link for the account
                                        logout(driver)
                                        driver = restart_browser(driver)
                                    
                        elif "Follow the profile below" in message.text:
                            links = extract_links(message.text)
                            if links:
                                link = links[0]
                                if last_link_per_account.get(account_username) != link:
                                    print(f"Extracted link for account {account_username}: {link}")
                                    if login(driver, current_account["username"], current_account["password"]):
                                        handle_notifications(driver)
                                        Follow(driver, link)
                                        client.send_message('https://t.me/SmmKingdomTasksBot', "✅Completed")
                                        print(f"'Follow' task completed for account {account_username}")
                                        last_link_per_account[account_username] = link  # Update the last link for the account
                                        logout(driver)
                                        driver = restart_browser(driver)
                                    
                        elif "Open the video, skip to the end" in message.text:
                            links = extract_links(message.text)
                            if links:
                                link = links[0]
                                if last_link_per_account.get(account_username) != link:
                                    driver.get(link)
                                    time.sleep(30)  # Wait until the video ends (adjust time if necessary)
                                    client.send_message('https://t.me/SmmKingdomTasksBot', "✅Completed")
                                    print(f"'Open the video, skip to the end' task completed for account {account_username}")
                                    last_link_per_account[account_username] = link  # Update the last link for the account
                                    driver = restart_browser(driver)
                        elif "Thank you for completing the task" in message.text:
                            print("Thank you message received.")
                        elif "View all Stories on the profile(just open the link and wait until all stories will be viewed) :" in message.text:
                            links = extract_links(message.text)
                            if links:
                                link = links[0]
                                if last_link_per_account.get(account_username) != link:
                                    driver.get(link)
                                    time.sleep(20)  # Wait until all stories are viewed (adjust time if necessary)
                                    client.send_message('https://t.me/SmmKingdomTasksBot', "✅Completed")
                                    print(f"'View all Stories' task completed for account {account_username}")
                                    last_link_per_account[account_username] = link  # Update the last link for the account
                                    driver = restart_browser(driver)
                        elif "Action :" in message.text and "Leave the comment" in message.text:
                            comment_match = re.search(r"💬 Comment :\n(.+)", message.text)
                            if comment_match:
                                comment = comment_match.group(1).strip()
                                print(f"Extracted comment for account {account_username}: {comment}")
                                # Send the comment here (add the function to comment if necessary)
                                client.send_message('https://t.me/SmmKingdomTasksBot', "✅Completed")
                                print(f"'Leave the comment' task completed for account {account_username}")
                                driver = restart_browser(driver)
                            else:
                                print("No comment found.")

                time.sleep(10)  # Wait 10 seconds before checking again
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                driver.quit()  # Close the browser in case of a severe error
                driver = restart_browser()
                continue  # Continue the script in case of a severe error

if __name__ == "__main__":
    main()
