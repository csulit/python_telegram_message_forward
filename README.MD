# How to Use the Program

To successfully set up and deploy this program, follow these step-by-step instructions:

1. **Create Configuration File:**
   - Begin by creating a new file named `config.yml`.
   - You can do this by copying the contents from an existing file named `config-sample.yml`. Ensure that you transfer all the content accurately to maintain the correct format and structure.

2. **Run the Script for Telegram Session:**
   - Once your `config.yml` file is set up, the next step is to run the script provided with the program.
   - This script is crucial as it creates a session for Telegram. Running it is mandatory before proceeding to the next steps. Ensure that the script executes without errors.

3. **Build the Docker Image:**
   - After setting up your Telegram session, your next task is to build the Docker image.
   - This step involves packaging the application with all its dependencies into a Docker container. It's a crucial step for deployment.

4. **Deploy to the Cloud:**
   - Now that your Docker image is ready, you can proceed to deploy this image to the cloud.
   - Choose your preferred cloud service provider and follow their specific instructions for Docker image deployment.

5. **Ensure Fixed Public IP for the Server:**
   - It's essential to make sure that the public IP address of your server is fixed (static).
   - A dynamic IP (one that changes) can cause a 'Telegram session error' due to multiple IP addresses being used.
   - If you're unsure how to set a static IP, consult your cloud service provider's documentation or help center.

6. **Monitor and Maintain:**
   - After deployment, monitor your application for any errors or performance issues.
   - Regularly check the logs and update the configuration as needed.

By following these instructions, you should be able to set up, deploy, and run the program without encountering significant issues. If you face any difficulties, refer to the program's documentation or seek assistance from community forums.
