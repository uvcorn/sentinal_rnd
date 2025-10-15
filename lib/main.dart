import 'package:flutter/material.dart';
import 'package:geocoding/geocoding.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Geocoding Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter Geocoding Example'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // ✅ Move these OUTSIDE build()
  final TextEditingController _zipController = TextEditingController();
  final TextEditingController _cityController = TextEditingController();
  final TextEditingController _stateController = TextEditingController();
  final TextEditingController _countryController = TextEditingController();

  String _coordinates = '';

  Future<void> _getCoordinates() async {
    try {
      String address = [
        _zipController.text.trim(),
        _cityController.text.trim(),
        _stateController.text.trim(),
        _countryController.text.trim(),
      ].where((e) => e.isNotEmpty).join(', ');

      if (address.isEmpty) {
        setState(() => _coordinates = 'Please enter at least one field.');
        return;
      }

      print('Fetching coordinates for: $address');

      final locations = await locationFromAddress(address);

      if (locations.isNotEmpty) {
        final loc = locations.first;
        setState(() {
          _coordinates =
              'Latitude: ${loc.latitude}, Longitude: ${loc.longitude}';
        });
        print(_coordinates);
      } else {
        setState(() {
          _coordinates = 'No results found for: $address';
        });
      }
    } catch (e, st) {
      setState(() {
        _coordinates = 'Error: $e';
      });
      debugPrint('Stack trace: $st');
    }
  }

  @override
  void dispose() {
    // ✅ Clean up controllers to avoid memory leaks
    _zipController.dispose();
    _cityController.dispose();
    _stateController.dispose();
    _countryController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildTextField(_zipController, 'Zip'),
              const SizedBox(height: 20),
              _buildTextField(_cityController, 'City'),
              const SizedBox(height: 20),
              _buildTextField(_stateController, 'State'),
              const SizedBox(height: 20),
              _buildTextField(_countryController, 'Country'),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _getCoordinates,
                child: const Text('Submit'),
              ),
              const SizedBox(height: 30),
              Text(
                _coordinates,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String hint) {
    return Container(
      width: 250,
      color: Colors.amber[100],
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
          hintText: hint,
          border: const OutlineInputBorder(),
          filled: true,
        ),
      ),
    );
  }
}
