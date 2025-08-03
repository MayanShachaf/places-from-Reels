import { useLocalSearchParams, router } from "expo-router";
import { useEffect } from "react";
import { View, Text } from "react-native";

export default function AuthRedirect() {
  const params = useLocalSearchParams();

  useEffect(() => {
    console.log("AuthRedirect params:", params); // Debug log
    router.replace({ pathname: "/", params }); // redirects to index with same query
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>AuthRedirect params: {JSON.stringify(params)}</Text>
    </View>
  );
}
