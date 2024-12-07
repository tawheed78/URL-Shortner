import time
import random
import snowflake
import string
from user_agents import parse

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def generate_custom_snowflake_id(param1, param2, sequence_length=12, epoch=1609459200000):
    # epoch = int(time.time() * 1000)
    config = snowflake.SnowflakeConfig(
        epoch=epoch,
        leading_bit=False,
        timestamp_length=42,
        param1_length=5,
        param2_length=5,
        sequence_length=sequence_length
    )
  
    SnowClass = snowflake.Snowflake(config)
    sequence_num = random.randint(0, (1 << sequence_length) - 1)
    custom_snowflake = SnowClass.generate_snowflake(param1=param1, param2=param2, sequence=sequence_num)
    return custom_snowflake

def convert_to_base62_encoding(unique_id):
    unique_id = int(unique_id)
    if unique_id == 0:
        return BASE62_ALPHABET[0]
    base62_str = ''
    while unique_id:
        unique_id, rem = divmod(unique_id, 62)
        base62_str = BASE62_ALPHABET[rem] + base62_str
    return base62_str

def generate_unique_short_code(datacenter_ID, machine_ID):
    snowflake_id = generate_custom_snowflake_id(datacenter_ID, machine_ID)
    short_code = convert_to_base62_encoding(snowflake_id)
    return short_code

def get_browser_and_device(user_agent):
    user_agent_data = parse(user_agent)
    browser = user_agent_data.browser.family.lower()
    if user_agent_data.is_mobile:
        device = "mobile"
    elif user_agent_data.is_tablet:
        device = "tablet"
    else:
        device = "pc"
    return browser, device