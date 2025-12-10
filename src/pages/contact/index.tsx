import React from 'react';
import Layout from '@theme/Layout';
import ContactForm from '@site/src/components/ContactForm';

export default function ContactPage() {
  return (
    <Layout title="Contact Us">
      <div className="container">
        <h1>Contact Us</h1>
        <p>Have a question? Fill out the form below to get in touch with us.</p>
        <ContactForm />
      </div>
    </Layout>
  );
}
