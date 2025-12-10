import React, { useState } from 'react';
import styles from './styles.module.css';

/**
 * A contact form component that allows users to send a message.
 * It includes fields for name, email, and message, and handles form submission.
 * @returns {JSX.Element} The contact form component.
 */
export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [emailError, setEmailError] = useState('');
  const [submissionStatus, setSubmissionStatus] = useState(null);

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateEmail(formData.email)) {
      setEmailError('Please enter a valid email address.');
      return;
    }
    setEmailError('');
    setSubmissionStatus('submitting');

    try {
      const response = await fetch('/api/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSubmissionStatus('success');
        setFormData({ name: '', email: '', message: '' });
      } else {
        setSubmissionStatus('error');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmissionStatus('error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.contactForm}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        {emailError && <p style={{ color: 'red' }}>{emailError}</p>}
      </div>
      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit" disabled={submissionStatus === 'submitting'}>
        {submissionStatus === 'submitting' ? 'Submitting...' : 'Submit'}
      </button>
      {submissionStatus === 'success' && (
        <p style={{ color: 'green' }}>Your message has been sent successfully!</p>
      )}
      {submissionStatus === 'error' && (
        <p style={{ color: 'red' }}>
          There was an error sending your message. Please try again later.
        </p>
      )}
    </form>
  );
}
