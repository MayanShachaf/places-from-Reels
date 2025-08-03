# 📍 Places From Reels

A fullstack app that helps users extract and save real-world places mentioned in Instagram Reels.

---

## 🧠 Project Summary

This project allows users to share Instagram Reels , extract location names using OpenAI, enrich place info using Google Maps API, and manage favorites locally using a backend powered by FastAPI and MongoDB.

---

## 🧱 Tech Stack

### 🌐 Backend (`/fastapi-backend`)
- **FastAPI** — Python web framework
- **MongoDB** — NoSQL database for user data and places
- **Google Maps API** — Fetches place details (address, rating, link)
- **OpenAI API** — Extracts location names from text

### 📱 Frontend (`/my-reel-map`)
- **React Native (Expo)** — Cross-platform mobile app
- **Axios** — Communicates with backend API
- **Google Maps integration** — Links to saved places

---

## 🚀 Features

- 🔗 Share Instagram Reels text
- 🧠 Automatically extract place names using AI
- 📍 Match with real places using Google Maps API
- ❤️ Save favorite places (per user)
- 🗺️ View and manage your favorite places
- 📱 Mobile-first design via React Native

