import time
import requests


def load_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://cats-frontend.tgapps.store"
    }

def process_user_info(auth, account_number):
    headers['Authorization'] = f"tma {auth}"
    response = requests.get("https://cats-backend-wkejfn-production.up.railway.app/user", headers=headers)

    if response.status_code == 200:
        data = response.json()
        username = data.get('username')
        total_rewards = data.get('totalRewards')
        print(f"Account #{account_number} ({username}) - {total_rewards} CATS")
        print(f"------------------------------------")
    else:
        print(f"Error fetching user info for account {account_number}: {response.status_code}")


def process_tasks(auth):
    headers['Authorization'] = f"tma {auth}"
    response = requests.get("https://cats-backend-wkejfn-production.up.railway.app/tasks/user", headers=headers)

    if response.status_code == 200:
        tasks = response.json().get("tasks", [])
        for task in tasks:
            task_id = task.get('id')
            title = task.get('title')
            reward_points = task.get('rewardPoints')
            completed = task.get('completed')
            allowCheck = task.get('allowCheck')

            if not completed:
                status_claim = f"#ID {task_id} - {title} - GET {reward_points} CATS -"
                time.sleep(1)
                if allowCheck == True:
                    check_task(auth, task_id, status_claim)
                else:
                    claim_task(auth, task_id, status_claim)
                
    else:
        print(f"Error fetching tasks: {response.status_code}")


def claim_task(auth, task_id, status_claim):
    headers['Authorization'] = f"tma {auth}"
    url = f"https://cats-backend-wkejfn-production.up.railway.app/tasks/{task_id}/complete"
    response = requests.post(url, headers=headers, json={})

    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"{status_claim} CLAIM DONE!!")
   

def check_task(auth, task_id, status_claim):
    headers['Authorization'] = f"tma {auth}"
    url = f"https://cats-backend-wkejfn-production.up.railway.app/tasks/{task_id}/check"
    response = requests.post(url, headers=headers, json={})

    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"{status_claim} CHECK DONE!!")
    

def main():
    list_auth = load_data('cats_query.txt')
    for index, auth in enumerate(list_auth, start=1):
        
        process_user_info(auth, index)
        process_tasks(auth)

    print('All Id Done')  
if __name__ == "__main__":
    main()