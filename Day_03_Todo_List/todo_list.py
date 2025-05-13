# To-Do List Manager 📝
# Concepts: Lists, Loops, Functions, User Input, String Formatting


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║       📝  TO-DO LIST MANAGER  📝       ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Add a Task                      │")
    print("  │   2  ➜  View All Tasks                  │")
    print("  │   3  ➜  Mark Task as Complete ✅        │")
    print("  │   4  ➜  Delete a Task                   │")
    print("  │   5  ➜  Clear All Tasks                 │")
    print("  │   6  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def show_tasks(tasks):
    print()
    if not tasks:
        print("  📭  Your to-do list is empty! Add some tasks.")
        print()
        return

    print("  ┌────────────────────────────────────────────────┐")
    print("  │               YOUR TASKS                        │")
    print("  ├────────────────────────────────────────────────┤")

    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "⏳"
        label = task["name"]
        if task["done"]:
            label = f"\033[9m{label}\033[0m"   # strikethrough for done tasks
        line = f"  │  {i:2}.  {status}  {task['name']}"
        if task["done"]:
            line = f"  │  {i:2}.  {status}  (Done) {task['name']}"
        # Truncate if too long
        max_len = 50
        if len(task["name"]) > max_len:
            display_name = task["name"][:max_len] + "..."
        else:
            display_name = task["name"]
        done_tag = "  ✔ Done" if task["done"] else ""
        print(f"  │  {i:2}.  {status}  {display_name}{done_tag}")

    completed = sum(1 for t in tasks if t["done"])
    pending = len(tasks) - completed
    print("  ├────────────────────────────────────────────────┤")
    print(f"  │  📊 Total: {len(tasks)}  |  ✅ Done: {completed}  |  ⏳ Pending: {pending}   ")
    print("  └────────────────────────────────────────────────┘")
    print()


def add_task(tasks):
    print()
    task_name = input("  ✏️  Enter task name: ").strip()
    if not task_name:
        print("  ⚠️  Task name cannot be empty!\n")
        return
    tasks.append({"name": task_name, "done": False})
    print(f"  ✅  Task added: \"{task_name}\"\n")


def mark_complete(tasks):
    if not tasks:
        print("\n  📭  No tasks to mark. Add some tasks first!\n")
        return

    show_tasks(tasks)
    pending = [(i, t) for i, t in enumerate(tasks) if not t["done"]]

    if not pending:
        print("  🎉  All tasks are already completed!\n")
        return

    while True:
        try:
            choice = int(input("  👉  Enter task number to mark complete (0 to cancel): "))
            if choice == 0:
                print("  ↩️  Cancelled.\n")
                return
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]
                if task["done"]:
                    print(f"  ℹ️  Task \"{task['name']}\" is already marked complete.\n")
                else:
                    task["done"] = True
                    print(f"  🎉  Great job! Task \"{task['name']}\" marked as complete!\n")
                return
            else:
                print(f"  ⚠️  Enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


def delete_task(tasks):
    if not tasks:
        print("\n  📭  No tasks to delete.\n")
        return

    show_tasks(tasks)
    while True:
        try:
            choice = int(input("  👉  Enter task number to delete (0 to cancel): "))
            if choice == 0:
                print("  ↩️  Cancelled.\n")
                return
            if 1 <= choice <= len(tasks):
                removed = tasks.pop(choice - 1)
                print(f"  🗑️  Deleted task: \"{removed['name']}\"\n")
                return
            else:
                print(f"  ⚠️  Enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


def clear_all(tasks):
    if not tasks:
        print("\n  📭  The list is already empty.\n")
        return

    confirm = input(f"\n  ⚠️  Are you sure you want to delete ALL {len(tasks)} task(s)? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        tasks.clear()
        print("  🧹  All tasks cleared!\n")
    else:
        print("  ↩️  Cancelled. Your tasks are safe.\n")


def main():
    show_banner()
    tasks = []

    while True:
        show_menu()
        choice = input("\n  👉  Select an option (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            mark_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            clear_all(tasks)
        elif choice == "6":
            completed = sum(1 for t in tasks if t["done"])
            print(f"\n  ════════════════════════════════════════")
            print(f"  👋  Goodbye! You completed {completed}/{len(tasks)} task(s) today.")
            print(f"  ════════════════════════════════════════\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 6.\n")


if __name__ == "__main__":
    main()
