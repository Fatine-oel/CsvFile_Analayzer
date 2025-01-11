from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd
import csv  # Pour détecter automatiquement le séparateur
from sklearn.preprocessing import LabelEncoder
def home(request):
    return render(request, 'gestion_fichiers/home.html')  # Affiche la page d'accueil


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Sauvegarder le fichier téléchargé
            # Charger le fichier CSV et détecter automatiquement le séparateur
            file_path = uploaded_file.file.path
            
            # Détecter automatiquement le séparateur
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(1024)  # Lire un échantillon du fichier pour détecter le séparateur
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter  # Détecter le délimiteur
            
            # Charger le fichier CSV avec le séparateur détecté
            data = pd.read_csv(file_path, sep=delimiter)
            
            # Sauvegarder les données dans la session sans encodage pour l'affichage initial
            request.session['file_data'] = data.to_dict()  # Sauvegarder les données dans la session
            return redirect('view_data')  # Rediriger vers la page qui affiche les données
    else:
        form = UploadFileForm()

    return render(request, 'gestion_fichiers/upload.html', {'form': form})

def view_data(request):
    # Récupérer les données du fichier à partir de la session
    data_dict = request.session.get('file_data')
    if not data_dict:
        return redirect('upload_file')  # Si aucune donnée, rediriger vers la page d'upload
    
    # Convertir le dictionnaire en DataFrame pandas
    data = pd.DataFrame.from_dict(data_dict)

    # Affichage des données sous forme de tableau sans encodage
    return render(request, 'gestion_fichiers/view_data.html', {'data': data})

def calculate_statistics(data, selected_column):
    if selected_column:
        column_data = data[selected_column]
        
        # Si la colonne est numérique, on calcule les statistiques classiques
        if column_data.dtype in ['float64', 'int64']:  
            stats = {
                'mean': column_data.mean(),
                'median': column_data.median(),
                'std_dev': column_data.std(),
                'min': column_data.min(),
                'max': column_data.max()
            }
        else:
            # Si la colonne est catégorielle, on calcule les statistiques adaptées
            stats = {
                'unique_values': column_data.unique(),
                'value_counts': column_data.value_counts().to_dict()
            }
        
        return stats
    return None

def stat_analysis(request):
    # Récupérer les données stockées dans la session
    data_dict = request.session.get('file_data')
    if not data_dict:
        return redirect('upload_file')  # Rediriger vers la page d'upload si aucune donnée n'est disponible
    
    # Convertir le dictionnaire en DataFrame pandas
    data = pd.DataFrame.from_dict(data_dict)

    # Encoder les valeurs catégoriques ici avant l'analyse statistique
    label_encoder = LabelEncoder()
    categorical_columns = data.select_dtypes(include=['object']).columns  # Trouver les colonnes catégorielles
    
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])  # Appliquer l'encodage sur chaque colonne catégorielle

    # Initialisation des variables pour l'analyse
    stats_results = None
    selected_column = None
    columns = data.columns.tolist()

    # Gestion des requêtes POST (lorsque l'utilisateur soumet un formulaire)
    if request.method == 'POST':
        selected_column = request.POST.get('column', None)  # Récupérer la colonne sélectionnée
        
        # Calculer les statistiques pour la colonne sélectionnée (column-wise)
        if selected_column:
            stats_results = calculate_statistics(data, selected_column)  # Appel correct de la fonction
    
    # Affichage de la page avec le formulaire et les résultats
    return render(request, 'gestion_fichiers/stat_analysis.html', {
        'data': data,
        'columns': columns,
        'stats_results': stats_results,
        'selected_column': selected_column  # Passer le nom de la colonne sélectionnée
    })

from django.shortcuts import render, redirect
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64

def visualisation(request):
    # Récupération des données stockées dans la session
    data_dict = request.session.get('file_data')
    if not data_dict:
        return redirect('upload_file')  # Rediriger si aucune donnée disponible

    # Conversion du dictionnaire en DataFrame
    data = pd.DataFrame.from_dict(data_dict)

    # Encoder les valeurs catégoriques ici avant la visualisation
    label_encoder = LabelEncoder()
    categorical_columns = data.select_dtypes(include=['object']).columns  # Trouver les colonnes catégorielles

    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])  # Appliquer l'encodage sur chaque colonne catégorielle

    charts = []  # Liste pour stocker les graphiques
    if request.method == 'POST':
        chart_type = request.POST.get('chart_type')
        selected_column = request.POST.get('column')
        x_column = request.POST.get('x_column')
        y_column = request.POST.get('y_column')

        # Gestion des graphiques avec Plotly pour l'interactivité
        fig = None  # Initialisation du graphique interactif
        if chart_type == 'histogram':
            fig = px.histogram(data, x=selected_column, title=f'Histogram of {selected_column}')
        elif chart_type == 'bar_chart':
            counts = data[selected_column].value_counts()
            fig = px.bar(x=counts.index, y=counts.values, labels={'x': selected_column, 'y': 'Count'},
                         title=f'Bar Chart of {selected_column}')
        elif chart_type == 'scatter_plot':
            fig = px.scatter(data, x=x_column, y=y_column, title=f'Scatter Plot of {x_column} vs {y_column}')
        elif chart_type == 'box_plot':
            fig = px.box(data, y=selected_column, title=f'Box Plot of {selected_column}')
        elif chart_type == 'violin_plot':
            fig = px.violin(data, y=selected_column, title=f'Violin Plot of {selected_column}')
        elif chart_type == 'line_chart':
            fig = px.line(data, x=data.index, y=selected_column, title=f'Line Chart of {selected_column}')
        elif chart_type == 'heatmap':
            corr_matrix = data.corr()
            fig = px.imshow(corr_matrix, text_auto=True, title='Heatmap of Correlations')
        elif chart_type == 'count_plot':
            # Transformer l'index en une colonne pour pouvoir l'utiliser dans Plotly
            counts = data[selected_column].value_counts().reset_index()
            counts.columns = [selected_column, 'count']  # Renommer les colonnes

            # Créer le graphique avec les colonnes appropriées
            fig = px.bar(counts, x=selected_column, y='count', 
                        labels={selected_column: 'Value', 'count': 'Count'},
                        title=f'Count Plot of {selected_column}')
        elif chart_type == 'kde_plot':
            fig = px.density_contour(data, x=selected_column, title=f'KDE Plot of {selected_column}')

        if fig:
            # Convertir le graphique en HTML pour l'inclure dans le template
            chart_html = fig.to_html(full_html=False)
            charts.append(chart_html)

    # Colonnes disponibles dans le DataFrame
    columns = data.columns.tolist()

    return render(request, 'gestion_fichiers/visualisation.html', {
        'charts': charts,
        'columns': columns
    })