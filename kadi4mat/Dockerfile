FROM dev-quay-registry.apps.k8sdevint.fzg.local/k8sdevint_corwiz-dev/library/ubuntu:22.10

# Install Apache HTTP Server
RUN apt-get update && apt-get install -y apache2

# Enable Apache modules
RUN a2enmod rewrite
RUN a2enmod headers

# Expose port 80 for Apache
EXPOSE 80

# Set the working directory
WORKDIR /var/www/html

# Start Apache as the main process
CMD ["apache2ctl", "-D", "FOREGROUND"]
