@app.route('/Live')
def transaction():
        # Start the background thread
        thread = Thread(target=generate_transaction)
        thread.start()

        # Immediately render the template
        return render_template('Live.html')
