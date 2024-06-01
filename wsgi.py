from app import app

if __name__ == '__main__':
    thread = threading.Thread(target=generate_transaction)
    thread.start()
    socketio.run(app, debug=True)