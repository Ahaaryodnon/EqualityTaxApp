import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { StatusBar } from 'expo-status-bar';

import HomeScreen from './screens/HomeScreen';
import PoliticiansScreen from './screens/PoliticiansScreen';
import BillionairesScreen from './screens/BillionairesScreen';
import PersonDetailScreen from './screens/PersonDetailScreen';
import AboutScreen from './screens/AboutScreen';

// Create Apollo Client
const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql', // Development URL, would be replaced in production
  cache: new InMemoryCache(),
});

// Create stack navigator
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <ApolloProvider client={client}>
      <NavigationContainer>
        <StatusBar style="auto" />
        <Stack.Navigator 
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#4F46E5', // Indigo-600
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Home" 
            component={HomeScreen} 
            options={{ title: 'Inequality App' }} 
          />
          <Stack.Screen 
            name="Politicians" 
            component={PoliticiansScreen}
          />
          <Stack.Screen 
            name="Billionaires" 
            component={BillionairesScreen} 
          />
          <Stack.Screen 
            name="PersonDetail" 
            component={PersonDetailScreen}
            options={({ route }) => ({ 
              title: route.params?.name || 'Person Details',
            })}
          />
          <Stack.Screen 
            name="About" 
            component={AboutScreen} 
          />
        </Stack.Navigator>
      </NavigationContainer>
    </ApolloProvider>
  );
} 