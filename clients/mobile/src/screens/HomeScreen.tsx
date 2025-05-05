import React, { useState } from 'react';
import { 
  StyleSheet, 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  Image,
  TextInput,
  ActivityIndicator
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useQuery } from '@apollo/client';
import { gql } from '@apollo/client';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';

// GraphQL query to fetch top politicians with highest passive income
const GET_TOP_POLITICIANS = gql`
  query GetTopPoliticians($limit: Int!) {
    persons(type: POLITICIAN, limit: $limit) {
      id
      fullName
      title
      constituency
      party
      yearlyPassiveIncome
      wealthTaxContribution
      photoUrl
    }
  }
`;

const HomeScreen = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigation = useNavigation();
  const { loading, error, data } = useQuery(GET_TOP_POLITICIANS, {
    variables: { limit: 5 },
  });

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      // In a real app, this would navigate to search results
      console.log('Searching for:', searchQuery);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        {/* Hero Section */}
        <View style={styles.heroSection}>
          <Text style={styles.heroTitle}>Financial Transparency</Text>
          <Text style={styles.heroSubtitle}>
            Discover how much passive income UK politicians and billionaires earn each year.
          </Text>

          {/* Search Bar */}
          <View style={styles.searchContainer}>
            <TextInput
              style={styles.searchInput}
              placeholder="Search for a politician or billionaire..."
              placeholderTextColor="#A0AEC0"
              value={searchQuery}
              onChangeText={setSearchQuery}
              onSubmitEditing={handleSearch}
            />
            <TouchableOpacity 
              style={styles.searchButton}
              onPress={handleSearch}
            >
              <Text style={styles.searchButtonText}>Search</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Top Politicians Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Top MPs by Passive Income</Text>

          {loading ? (
            <ActivityIndicator size="large" color="#4F46E5" />
          ) : error ? (
            <Text style={styles.errorText}>Error loading data. Please try again.</Text>
          ) : (
            <View style={styles.politiciansContainer}>
              {data?.persons.map((person) => (
                <TouchableOpacity
                  key={person.id}
                  style={styles.personCard}
                  onPress={() => 
                    navigation.navigate('PersonDetail', {
                      id: person.id,
                      name: person.fullName
                    })
                  }
                >
                  <View style={styles.personImageContainer}>
                    {person.photoUrl ? (
                      <Image
                        source={{ uri: person.photoUrl }}
                        style={styles.personImage}
                      />
                    ) : (
                      <View style={styles.personImagePlaceholder}>
                        <Text style={styles.personImagePlaceholderText}>
                          {person.fullName.charAt(0)}
                        </Text>
                      </View>
                    )}
                  </View>
                  
                  <View style={styles.personInfo}>
                    <Text style={styles.personName}>
                      {person.title ? `${person.title} ` : ''}
                      {person.fullName}
                    </Text>
                    
                    {(person.constituency || person.party) && (
                      <Text style={styles.personSubtitle}>
                        {person.constituency}
                        {person.constituency && person.party ? ' • ' : ''}
                        {person.party}
                      </Text>
                    )}
                    
                    <View style={styles.personFinancials}>
                      <Text style={styles.personFinancialsLabel}>
                        Yearly Passive Income:
                      </Text>
                      <Text style={styles.personFinancialsValue}>
                        {formatCurrency(person.yearlyPassiveIncome)}
                      </Text>
                    </View>
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          )}

          <TouchableOpacity
            style={styles.viewAllButton}
            onPress={() => navigation.navigate('Politicians')}
          >
            <Text style={styles.viewAllButtonText}>View All Politicians</Text>
          </TouchableOpacity>
        </View>

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Why Financial Transparency Matters</Text>
          
          <Text style={styles.paragraphText}>
            Financial transparency in politics is essential for democracy. When politicians 
            have significant financial interests, the public deserves to know about potential 
            conflicts of interest.
          </Text>
          
          <Text style={styles.paragraphText}>
            The Inequality App collects data from official sources including:
          </Text>
          
          <View style={styles.bulletList}>
            <Text style={styles.bulletItem}>• UK Parliament's Register of Members' Financial Interests</Text>
            <Text style={styles.bulletItem}>• Companies House filings</Text>
            <Text style={styles.bulletItem}>• Land Registry records</Text>
            <Text style={styles.bulletItem}>• Forbes billionaire valuations</Text>
          </View>
        </View>
      </ScrollView>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  scrollContainer: {
    paddingBottom: 40,
  },
  heroSection: {
    padding: 20,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 10,
    textAlign: 'center',
  },
  heroSubtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.9)',
    marginBottom: 20,
    textAlign: 'center',
  },
  searchContainer: {
    width: '100%',
    flexDirection: 'row',
    marginTop: 10,
  },
  searchInput: {
    flex: 1,
    height: 50,
    backgroundColor: 'white',
    borderRadius: 25,
    paddingHorizontal: 20,
    fontSize: 16,
  },
  searchButton: {
    marginLeft: 10,
    height: 50,
    backgroundColor: '#3730A3',
    borderRadius: 25,
    paddingHorizontal: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 20,
    textAlign: 'center',
  },
  politiciansContainer: {
    marginBottom: 20,
  },
  personCard: {
    backgroundColor: 'white',
    borderRadius: 10,
    marginBottom: 15,
    flexDirection: 'row',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    overflow: 'hidden',
  },
  personImageContainer: {
    width: 100,
    height: 100,
  },
  personImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  personImagePlaceholder: {
    width: '100%',
    height: '100%',
    backgroundColor: '#EEF2FF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  personImagePlaceholderText: {
    fontSize: 28,
    color: '#6366F1',
  },
  personInfo: {
    flex: 1,
    padding: 12,
    justifyContent: 'center',
  },
  personName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  personSubtitle: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 8,
  },
  personFinancials: {
    marginTop: 4,
  },
  personFinancialsLabel: {
    fontSize: 13,
    color: '#6B7280',
  },
  personFinancialsValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
  },
  viewAllButton: {
    backgroundColor: '#4F46E5',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 10,
    alignSelf: 'center',
  },
  viewAllButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  errorText: {
    color: '#DC2626',
    textAlign: 'center',
    marginVertical: 20,
  },
  paragraphText: {
    fontSize: 16,
    color: '#4B5563',
    lineHeight: 24,
    marginBottom: 15,
  },
  bulletList: {
    marginTop: 5,
    marginBottom: 15,
  },
  bulletItem: {
    fontSize: 16,
    color: '#4B5563',
    lineHeight: 24,
    marginBottom: 8,
    paddingLeft: 5,
  },
});

export default HomeScreen; 