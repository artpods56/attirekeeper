# AttireKeeper 🧦

AttireKeeper is an advanced inventory management system designed to organize and enhance your clothing listings for online sales. Built with Django, FastAPI, PostgreSQL, and Docker, this application offers a range of features to streamline your inventory processes and improve your online presence.

## Features

- **Full CRUD Operations**: Create, read, update, and delete functionality for your inventory.
- **Description Templates**: Create and manage templates for product descriptions.
- **Listing Browsing**: Easily browse and search through your inventory listings.
- **Background Removal**: Seamlessly remove image backgrounds using an AI model.
- **Photo Augmentation**: Modify listing photos to avoid recognition issues on e-commerce platforms.
- **Analytics**: Coming soon - powerful analytic features to track and optimize your sales.

## Tech Stack

- 🧢 **Backend**: Django, FastAPI, PyTorch
- 👕 **Frontend**: Django, Bootstrap5
- 👖 **Database**: PostgreSQL
- 👟 **Containerization**: Docker

## AI Model for Background Removal

We utilize the [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) model for image background removal. Special thanks to [ZhengPeng7](https://github.com/ZhengPeng7) for his outstanding work on this model. We highly recommend checking out his project.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/artpods56/attirekeeper.git
    cd attirekeeper
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

    or execute the `run_container.bat` script.

## Usage:
- Access the Django web application at `http://localhost:8001/hub`.
- Check the FastAPI documentation at `http://localhost:8000/docs`).


## License

This project is licensed under the MIT License. See the LICENSE file for more details.


---

Happy selling with **AttireKeeper**! 🛍️
