PopupMenuButton<String>(
  tooltip: context.l10n.settingsMenu, 
  itemBuilder: (context) => [
    PopupMenuItem(
      value: 'profile',
      child: ListTile(
        leading: Icon(Icons.person),
        title: Text(context.l10n.profile),
      ),
      semanticsLabel: 'Open profile settings', 
    ),



    PopupMenuItem(
      value: 'privacy',
      child: ListTile(
        leading: Icon(Icons.security),
        title: Text(context.l10n.privacy),
        subtitle: Text(context.l10n.managePrivacySettings),
      ),
    ),
  ],


  
  onSelected: (value) {
    if (value == 'profile') Navigator.pushNamed(context, '/profile');
    if (value == 'privacy') Navigator.pushNamed(context, '/privacy');
  },
)