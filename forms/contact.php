<?php
  /**
  * Requires the "PHP Email Form" library
  * The "PHP Email Form" library is available only in the pro version of the template
  * The library should be uploaded to: vendor/php-email-form/php-email-form.php
  * For more info and help: https://bootstrapmade.com/php-email-form/
  */

  // Replace system@example.com with your real receiving email address
  $receiving_email_address = 'system@example.com';

  if( file_exists($php_email_form = '../assets/vendor/php-email-form/php-email-form.php' )) {
    include( $php_email_form );
  } else {
    die( 'Unable to load the "PHP Email Form" Library!');
  }

  $system = new PHP_Email_Form;
  $system->ajax = true;
  
  $system->to = $receiving_email_address;
  $system->from_name = $_POST['name'];
  $system->from_email = $_POST['email'];
  $system->subject = $_POST['subject'];

  // Uncomment below code if you want to use SMTP to send emails. You need to enter your correct SMTP credentials
  /*
  $system->smtp = array(
    'host' => 'example.com',
    'username' => 'example',
    'password' => 'pass',
    'port' => '587'
  );
  */

  $system->add_message( $_POST['name'], 'From');
  $system->add_message( $_POST['email'], 'Email');
  $system->add_message( $_POST['message'], 'Message', 10);

  echo $system->send();
?>
