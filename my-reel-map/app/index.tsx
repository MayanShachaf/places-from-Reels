import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { addUser } from "../api/api"; // Adjust the import path as necessary
import { useRouter } from "expo-router";
import { usePathname} from "expo-router";
// This is the login screen component
const LoginScreen = () => {
  const router = useRouter();
  
  // State for user input
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [id, setId] = useState("");
  // Function to handle login
  const handleLogin = () => {
    if (!name || !email) {
      alert("Please enter both name and email.");
      return;
    }
    
    addUser(name, email)
      .then((data) => {
        setId(data.id)
        router.push({
        pathname: "./user/list_screen",
        params: { id : data.id },
});
      })
      .catch((error) => {
        console.error("Error adding user:", error);
      });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hi!!! Sign In</Text>
      <TextInput
        style={styles.input}
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
      />
      <Button title="Login" onPress={handleLogin} />
    </View>
  
    );
};

export default LoginScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
    textAlign: "center",
  },
  input: {
    borderBottomWidth: 1,
    padding: 10,
    marginBottom: 20,
  },
});
