# Research: Add Contact Form

## Email Sending Service

**Decision**: Use **Nodemailer** with **SendGrid**.

**Rationale**:
- **Nodemailer** is a popular, open-source Node.js library with zero dependencies for sending emails. It's flexible and supports various transport methods, including SMTP.
- **SendGrid** is a popular email service provider with a generous free tier (3,000 emails per month) and a robust API.
- This combination is widely used and recommended by the community.

**Alternatives considered**:
- Mailjet
- MailerSend
- Maileroo
- Amazon SES

## Testing Strategy

**Decision**: Use **React Testing Library** and **Jest** for unit and integration testing.

**Rationale**:
- **React Testing Library (RTL)** and **Jest** are the standard and recommended tools for testing React applications.
- They allow testing components from the user's perspective, which makes the tests more robust and maintainable.
- Docusaurus is built with React, so these tools are a natural fit.

**Alternatives considered**:
- **Cypress** and **Playwright** for end-to-end (E2E) testing. These can be added later if needed to test the full user flow.
