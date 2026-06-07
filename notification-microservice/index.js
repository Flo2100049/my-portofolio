require('dotenv').config();
const amqp = require('amqplib');
const sgMail = require('@sendgrid/mail');
const twilio = require('twilio');

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const QUEUE_NAME = 'contact_requests';
const RABBITMQ_URL = process.env.RABBITMQ_URL;

const twilioClient = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

async function sendEmailNotification(data) {
    const msg = {
        to: process.env.MY_EMAIL,
        from: process.env.MY_EMAIL,
        subject: `New Portfolio Contact from ${data.name}`,
        text: `You received a new message from ${data.email}:\n\n${data.message}`,
    };

    try {
        await sgMail.send(msg);
        console.log('Email sent successfully to', process.env.MY_EMAIL);
    } catch (error) {
        console.error('Error sending email:', error);
    }
}

async function sendWhatsAppNotification(data) {
    try {
        const message = await twilioClient.messages.create({
            from: `whatsapp:${process.env.TWILIO_WHATSAPP_NUMBER}`,
            to: `whatsapp:${process.env.MY_WHATSAPP_NUMBER}`,
            body: `🚀 *Νέο Μήνυμα στο Portfolio!*\n\n*Από:* ${data.name}\n*Email:* ${data.email}\n*Μήνυμα:*\n${data.message}`
        });
        console.log('WhatsApp sent successfully! Message SID:', message.sid);
    } catch (error) {
        console.error('Error sending WhatsApp:', error.message);
    }
}

async function connectToRabbitMQ() {
    let connection;
    while (!connection) {
        try {
            console.log("Attempting to connect to RabbitMQ...");
            connection = await amqp.connect(RABBITMQ_URL);
            console.log("Successfully connected to RabbitMQ!");
        } catch (err) {
            console.log("RabbitMQ not ready yet. Retrying in 5 seconds...");
            await new Promise(res => setTimeout(res, 5000));
        }
    }

    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: true });

    console.log(`🎧 Worker is listening for messages in '${QUEUE_NAME}'...`);

    channel.consume(QUEUE_NAME, async (msg) => {
        if (msg !== null) {
            const messageData = JSON.parse(msg.content.toString());
            console.log("📥 Received new message:", messageData);

            await sendEmailNotification(messageData);
            await sendWhatsAppNotification(messageData);

            channel.ack(msg);
            console.log("Message acknowledged and removed from queue.\n");
        }
    });
}

connectToRabbitMQ();