# How to Deploy to Vercel

I have prepared your project for Vercel deployment by creating `vercel.json` and `requirements.txt`.

Since the Vercel CLI is not currently installed in your environment, you have two options to deploy:

## Option 1: Install Node.js and Vercel CLI (Recommended)

1.  **Install Node.js**: Download and install from [nodejs.org](https://nodejs.org/).
2.  **Install Vercel CLI**: Open your terminal (PowerShell or Command Prompt) and run:
    ```bash
    npm install -g vercel
    ```
3.  **Deploy**:
    Navigate to the project folder:
    ```bash
    cd "c:\Users\SHREESHA012\OneDrive\Desktop\Shreesha Docs\Shreesha Portfolio\flask_snake_game"
    ```
    Run the deploy command:
    ```bash
    vercel
    ```
    Follow the on-screen prompts (login, confirm project settings).

## Option 2: Deploy via GitHub

1.  **Push to GitHub**: Create a new repository on GitHub and push this code to it.
2.  **Connect to Vercel**:
    - Go to [vercel.com](https://vercel.com) and log in.
    - Click "Add New..." -> "Project".
    - Import your GitHub repository.
    - Vercel will automatically detect the `vercel.json` and deploy your game.

## Configuration Details

-   **requirements.txt**: Lists `Flask` as a dependency.
-   **vercel.json**: Tells Vercel to use the Python runtime for `app.py`.
