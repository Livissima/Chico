import jpype
import os

# Lista de caminhos possíveis do JRE no Windows
jre_paths = [
    "C:\\Program Files\\Java\\jre1.8.0_451\\bin\\server\\jvm.dll",
    "C:\\Program Files (x86)\\Java\\jre1.8.0_451\\bin\\server\\jvm.dll",
    "C:\\Program Files\\Java\\jre1.8.0\\bin\\server\\jvm.dll",
    os.path.join(os.environ.get('JAVA_HOME', ''), 'bin', 'server', 'jvm.dll'),
]

for path in jre_paths:
    if os.path.exists(path):
        try:
            jpype.startJVM(path)
            print(f"JVM iniciado com sucesso usando: {path}")
            break
        except Exception as e:
            print(f"Falha com {path}: {e}")
else:
    print("Nenhum JVM encontrado. Tentando método padrão...")
    try:
        jpype.startJVM(jpype.getDefaultJVMPath())
        print("JVM iniciado com método padrão")
    except Exception as e:
        print(f"Erro final: {e}")