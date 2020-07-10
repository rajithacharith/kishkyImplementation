from google.cloud import translate_v2 as translate
translate_client = translate.Client()
import six

eng = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
"you", "your", "yours", "yourself", "yourselves", "he", "him", "his", 
"himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", 
"them", "their", "theirs", "themselves", "what", "which", "who", "whom", 
"this", "that", "these", "those", "am", "is", "are", "was", "were", "be", 
"been", "being", "have", "has", "had", "having", "do", "does", "did", 
"doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", 
"until", "while", "of", "at", "by", "for", "with", "about", "against", 
"between", "into", "through", "during", "before", "after", "above", "below", 
"to", "from", "up", "down", "in", "out", "on", "off", "over", "under", 
"again", "further", "then", "once", "here", "there", "when", "where", "why", 
"how", "all", "any", "both", "each", "few", "more", "most", "other", "some", 
"such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", 
"s", "t", "can", "will", "just", "don", "should", "now"]

if isinstance(eng, six.binary_type):
    eng = eng.decode('utf-8')

result = translate_client.translate(
    eng, target_language="si")
print(result)
a = []
for resulti in result:
    a.append(resulti['translatedText'])

print(a)