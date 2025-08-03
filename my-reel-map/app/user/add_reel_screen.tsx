import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  StyleSheet,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import { addPlace } from "../../api/api";

const AddReelScreen = () => {
  const [reelText, setReelText] = useState("");
  const router = useRouter();
  const { userId } = useLocalSearchParams(); // ✅ matches what you sent
  const user_Id = Array.isArray(userId) ? userId[0] : userId ?? "";
  const handleSubmit = async () => {
    if (!reelText.trim()) {
      alert("Please enter text!");
      return;
    }
    if (!user_Id) {
      alert("no userId found");
      return;
    }
    try {
      const newPlace = await addPlace(user_Id, reelText);
      if (!newPlace || newPlace.name === "unknown") {
        alert("sorry! can't find this place ");
      }
      if (newPlace.name !== "unknown") {
        router.push({
          pathname: "./place_details_screen",
          params: {
            name: newPlace.name,
            city: newPlace.city,
            address_hint: newPlace.address_hint,
            type: newPlace.type,
            summarize: newPlace.summarize,
            google_maps_url: newPlace.google_maps_url,
            rating: newPlace.rating,
          },
        });
      }
      setReelText("");

      //router.back();
    } catch (error) {
      console.error("Error adding place:", error);
      alert("Something went wrong");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Paste your reel text below</Text>
      <TextInput
        style={styles.input}
        placeholder="Reel text"
        multiline
        value={reelText}
        onChangeText={setReelText}
        textAlignVertical="top"
      />
      <View style={styles.buttonWrapper}>
        <Button title="Add Place" onPress={handleSubmit} />
      </View>
    </View>
  );
};

export default AddReelScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "flex-start",
  },
  title: {
    fontSize: 22,
    marginBottom: 12,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 6,
    padding: 12,
    minHeight: 120,
    fontSize: 16,
    marginBottom: 20,
  },
  buttonWrapper: {
    marginTop: 10,
  },
});
