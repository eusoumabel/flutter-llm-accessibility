PopupMenuButton<String>(
  
  itemBuilder: (context) => [
    PopupMenuItem(
      value: 'p', 
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.person, size: 16),  
          SizedBox(width: 2),  
          Text('P'),  
        ],
      ),
    ),
    PopupMenuItem(
      value: 's', 
      child: Icon(Icons.security, size: 16), 
    ),
    PopupMenuItem(
      value: 'i', 
      child: Padding(
        padding: EdgeInsets.zero, 
        child: Text('Info', style: TextStyle(fontSize: 12)), 
      ),
    ),
  ],
  onSelected: (value) {
    switch (value) {
      case 'p': Navigator.pushNamed(context, '/profile'); break;
      case 's': Navigator.pushNamed(context, '/privacy'); break;
      case 'i': showAboutDialog(context); break;
    }
  },
  icon: Icon(Icons.more_vert, size: 18),
  offset: Offset(0, 30),
)