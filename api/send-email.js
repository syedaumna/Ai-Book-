const sgMail = require('@sendgrid/mail');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Only POST requests allowed' });
  }

  const { name, email, message } = req.body;

  // It's good practice to validate the input on the server side as well
  if (!name || !email || !message) {
    return res.status(400).json({ message: 'Name, email, and message are required' });
  }

  // Set SendGrid API key
  // IMPORTANT: Replace with your actual SendGrid API key
  // It's best to use an environment variable for this
  sgMail.setApiKey(process.env.SENDGRID_API_KEY || 'YOUR_SENDGRID_API_KEY');

  const msg = {
    to: 'your-email@example.com', // Change to your recipient
    from: 'your-verified-sender@example.com', // Change to your verified sender
    subject: `New contact from ${name}`,
    text: message,
    html: `<strong>From:</strong> ${name} <br/> <strong>Email:</strong> ${email} <br/> <strong>Message:</strong> ${message}`,
  };

  try {
    await sgMail.send(msg);
    res.status(200).json({ message: 'Email sent successfully' });
  } catch (error) {
    console.error(error);
    if (error.response) {
      console.error(error.response.body);
    }
    res.status(500).json({ message: 'Error sending email' });
  }
}
