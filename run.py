from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="10.60.163.239", debug=True)
