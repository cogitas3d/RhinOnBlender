bl_info = {
    "name": "RhinOnBlender",
    "author": "Cicero Moraes, Pablo Maricevich, Rodrigo Dornelles e Everton da Rosa",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D",
    "description": "Planejamento de Rinoplastia no Blender",
    "warning": "",
    "wiki_url": "",
    "category": "rhin",
    }

import bpy
from math import sqrt
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


# MOSTRA/OCULTA FACE

def RhinMostraOcultaFaceDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.data.objects["face_copia"].hide = not bpy.data.objects["face_copia"].hide


class RhinMostraOcultaFace(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.mostra_oculta_face"
    bl_label = "Mostra Oculta Face"
    
    def execute(self, context):
        RhinMostraOcultaFaceDef(self, context)
        return {'FINISHED'}


# LINHA BASE

def RhinLinhaBaseDef(self, context):

    verts = [Vector((0, 0, 125)),
             Vector((0, 0, -125)),
            ]

    edges = [[0,1]]
    
    faces = []


    mesh = bpy.data.meshes.new(name="LinhaBase")
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)
    

class RhinLinhaBase(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_linhabase"
    bl_label = "Add Linha Base"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        RhinLinhaBaseDef(self, context)

        return {'FINISHED'}

def add_object_button(self, context):
    self.layout.operator(
        RhinLinhaBase.bl_idname,
        text="LinhaBase",
        icon='VIEW3D')

# PIVO CURSOR

def RhinPivoCursorDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.context.space_data.pivot_point = 'CURSOR'

class RhinPivoCursor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.pivo_cursor"
    bl_label = "Pivô Cursor"
    
    def execute(self, context):
        RhinPivoCursorDef(self, context)
        return {'FINISHED'}


# CRIA ESPESSURA GUIA

def RhinCriaEspessuraDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.object.modifier_add(type='SOLIDIFY') 
    bpy.context.object.modifiers["Solidify"].thickness = 4
    bpy.context.object.modifiers["Solidify"].offset = 1

class RhinCriaEspessura(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.cria_espessura"
    bl_label = "Cria Espessura"
    
    def execute(self, context):
        RhinCriaEspessuraDef(self, context)
        return {'FINISHED'}

# ESCULTURA GRAB

def RhinEsculturaGrabDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.paint.brush_select(paint_mode='SCULPT', sculpt_tool='GRAB')
    bpy.ops.brush.curve_preset(shape='ROOT')

class RhinEsculturaGrab(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.escultura_grab"
    bl_label = "Escultura Grab"
    
    def execute(self, context):
        RhinEsculturaGrabDef(self, context)
        return {'FINISHED'}

# CRIA COPIA ROSTO

def RhinRhinRostoCriaCopiaDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene
    
    obj.name="face"

    bpy.ops.object.duplicate()
  
    obj2 = context.active_object
 
    obj2.name="face_copia"
    obj2.hide = True


class RhinRostoCriaCopia(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.rosto_cria_copia"
    bl_label = "Rosto Cria Copia"
    
    def execute(self, context):
        RhinRostoCriaCopiaDef(self, context)
        return {'FINISHED'}

# DISTANCIA OBJETOS    

def RhinDistanciaObjetosDef(self, context):
    """
    return: float. Distance of the two objects
    Must select two objects
    """
    l = []
    CimaMeio = [bpy.data.objects['MarcaMeio'], bpy.data.objects['MarcaTopo']]
    
    for item in CimaMeio:
       l.append(item.location)

    distanciaMaior = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
    print(distanciaMaior)  # print distance to console, DEBUG

    l2 = []
    MeioBaixo = [bpy.data.objects['MarcaMeio'], bpy.data.objects['MarcaBaixo']]

    for item in MeioBaixo:
       l2.append(item.location)

    distanciaMenor = sqrt( (l2[0][0] - l2[1][0])**2 + (l2[0][1] - l2[1][1])**2 + (l2[0][2] - l2[1][2])**2)
    print(distanciaMenor)  # print distance to console, DEBUG

    Fator = distanciaMenor / distanciaMaior
    print(Fator)
    
    bpy.data.objects["Text"].data.body = str(Fator)

    return Fator

#get_distance()

class RhinDistanciaObjetos(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.distancia_objetos"
    bl_label = "Distância Objetos"
    
    def execute(self, context):
        RhinDistanciaObjetosDef(self, context)
        return {'FINISHED'}


# ZOOM
class RhinZoomCena(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Zoom Cena"
    bl_idname = "rhin_zoom_cena"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("view3d.viewnumpad", text="Frente").type='FRONT'
        row.operator("view3d.viewnumpad", text="Atrás").type='BACK'
        
        row = layout.row()
        row.operator("view3d.viewnumpad", text="Direita").type='RIGHT'
        row.operator("view3d.viewnumpad", text="Esquerda").type='LEFT'
        
        row = layout.row()
        row.operator("view3d.viewnumpad", text="Cima").type='TOP'
        row.operator("view3d.viewnumpad", text="Baixo").type='BOTTOM'
        
        row = layout.row()
        row.operator("opr.pan_down_view1", text="Pan", icon="TRIA_UP")
        row.operator("opr.pan_up_view1", text="Pan", icon="TRIA_DOWN")
        row.operator("opr.pan_right_view1", text="Pan", icon="TRIA_LEFT")
        row.operator("opr.pan_left_view1", text="Pan", icon="TRIA_RIGHT")

        row = layout.row()
        row.operator("opr.orbit_down_view1", text="Orb", icon="FILE_PARENT")
        row.operator("opr.orbit_up_view1", text="Orb", icon="FILE_REFRESH")
        row.operator("opr.orbit_right_view1", text="Orb", icon="LOOP_BACK")
        row.operator("opr.orbit_left_view1", text="Orb", icon="LOOP_FORWARDS")

        
        row = layout.row()
        row.operator("view3d.view_persportho", text="Persp/Orto")
        row.operator("view3d.view_all", text="Centraliza Zoom", icon="VIEWZOOM").center=False    

# FOTOGRAMETRIA

class RhinCriaFotogrametria(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Cria Fotogrametria"
    bl_idname = "rhin_cria_fotogrametria"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object 
        
        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="")
 
        row = layout.row()
        row.operator("object.gera_modelo_foto", text="Iniciar Fotogrametria", icon="IMAGE_DATA")

        row = layout.row()
        row.operator("object.gera_modelo_foto_smvs", text="SMVS+Meshlab", icon="IMAGE_DATA")

# IMPORTA FOTOGRAMETRIA

class RhinImportaFotogrametria(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Importar Fotogrametria"
    bl_idname = "rhin_importa_fotogrametria"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("import_scene.obj", text="Importa OBJ", icon="MOD_MASK")

class RhinAlinhaFaces(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Alinha Faces"
    bl_idname = "rhin_alinha_faces"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        layout.operator("object.alinha_rosto", text="1 - Alinha com a Camera", icon="MANIPUL")
        col = self.layout.column(align = True)
        col.prop(context.scene, "medida_real")  
        layout.operator("object.alinha_rosto2", text="2 - Alinha e Redimensiona", icon="LAMP_POINT")


# ESTUDA FACE

class RhinEstudaFaces(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Estuda Faces"
    bl_idname = "rhin_estuda_faces"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Central Ver", icon="PAUSE")
        linha.location=(0,-200,0)

        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Central Hor", icon="ZOOMOUT")
        linha.location=(0,-200,0)
        linha.rotation=(0,1.5708,0)
        
        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Lateral Hor", icon="ZOOMOUT")
        linha.location=(200,30,0)
        linha.rotation=(1.5708,0,0)

#        row = layout.row()
#        row.operator("object.align_picked_points", text="Alinha por Pontos", icon="PARTICLE_TIP")



# REDIMENSIONAMENTO
   
class RhinRedimensionamento(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Redimensionamento"
    bl_idname = "rhin_redimensionamento"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("measureit.runopenglbutton", text="Ver/Ocultar Medidas", icon="ARROW_LEFTRIGHT")


        row = layout.row()
        row.operator("measureit.addsegmentbutton", text="Fazer Medida", icon="CURVE_NCURVE")

        row = layout.row()
        row.operator("measureit.addanglebutton", text="Medir Ângulo", icon="EDITMODE_VEC_DEHLT")
        
        row = layout.row()
        row.operator("view3d.ruler", text="Medida/Ângulo Rápido", icon="IPO_LINEAR")
        
                
# SEPARAR FACE
   
class RhinSeparaFace(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Separar Face"
    bl_idname = "rhin_separa_face"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        circle=row.operator("mesh.primitive_circle_add", text="Círculo de Corte", icon="MESH_CIRCLE")
        circle.radius=200
        circle.vertices=100
        circle.location=(135,-185,0)
        circle.rotation=(0,1.5708,0)
        
        row = layout.row()
        knife=row.operator("object.corta_face", text="Cortar!", icon="META_PLANE")
        
        row = layout.row()
        circle=row.operator("object.rosto_cria_copia", text="Copia Face", icon="NODETREE")
        
        
# ESTUDO DE ESTRUTURA
   
class RhinEstudoEstrutura(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Estudo de Estrutura"
    bl_idname = "rhin_estudo_estrutura"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"
    

    def draw(self, context):
        layout = self.layout

        obj = context.object
                
        row = layout.row()
        row.operator("object.distancia_objetos", text="Fator do Nariz", icon="STICKY_UVS_DISABLE")

        row = layout.row()
        row.operator("view3d.snap_cursor_to_selected", text="Pivô para Seleção", icon="RESTRICT_SELECT_OFF")
        
        row = layout.row()
        row.operator("object.pivo_cursor", text="Pivô no Cursor", icon="CURSOR")
        

#bpy.context.space_data.pivot_point = 'CURSOR'

        
        
# ESCULPIR
      
class RhinEscultura(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Escultura"
    bl_idname = "rhin_escultura"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("object.mode_set", text="Modo Objeto", icon="OBJECT_DATA").mode = 'OBJECT'
        
        row = layout.row()
        row.operator("sculpt.sculptmode_toggle", text="Modo Escultura", icon="SCULPTMODE_HLT")
        
        row = layout.row()
        row.operator("object.escultura_grab", text="Agarra", icon="BRUSH_GRAB")
 
        row = layout.row()
        row.operator("paint.brush_select", text="Empurra", icon="BRUSH_NUDGE").sculpt_tool='NUDGE'
        
        row = layout.row()
        row.operator("paint.brush_select", text="Desenha", icon="BRUSH_SCULPT_DRAW").sculpt_tool='DRAW'
        
        row = layout.row()
        row.operator("paint.brush_select", text="Alisa", icon="BRUSH_SMOOTH").sculpt_tool='SMOOTH'

# PRE E PÓS

class RhinPrePos(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Pré e Pós"
    bl_idname = "rhin_pre_pos"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("object.mostra_oculta_face", text="Mostra/Oculta Face", icon="MOD_MASK")

        row = layout.row()
        row.operator("view3d.clip_border", text="Cria Filete", icon="UV_FACESEL")

# DESENHA GUIA
   
class RhinDesenhaGuia(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Desenha Guia"
    bl_idname = "rhin_desenha_guia"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("cut_mesh.polytrim", text="Desenha Cortes", icon="OUTLINER_DATA_MESH")
        
        row = layout.row()
        circle=row.operator("object.cria_espessura", text="Cria Espessura", icon="MOD_SOLIDIFY")
        
        row = layout.row()
        row.operator("object.prepara_impressao", text="Prepara Impressão 3D", icon="MOD_REMESH")       


def register():
    bpy.utils.register_class(RhinMostraOcultaFace)
    bpy.utils.register_class(RhinLinhaBase)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)
    bpy.utils.register_class(RhinPivoCursor)
    bpy.utils.register_class(RhinCriaEspessura)
    bpy.utils.register_class(RhinEsculturaGrab)
    bpy.utils.register_class(RhinRostoCriaCopia)
    bpy.utils.register_class(RhinDistanciaObjetos)
    bpy.utils.register_class(RhinZoomCena)
    bpy.utils.register_class(RhinCriaFotogrametria)
    bpy.utils.register_class(RhinImportaFotogrametria)
    bpy.utils.register_class(RhinAlinhaFaces)
    bpy.utils.register_class(RhinEstudaFaces)
    bpy.utils.register_class(RhinRedimensionamento)
    bpy.utils.register_class(RhinSeparaFace)
    bpy.utils.register_class(RhinEstudoEstrutura)
    bpy.utils.register_class(RhinEscultura)
    bpy.utils.register_class(RhinPrePos)
    bpy.utils.register_class(RhinDesenhaGuia)

    

def unregister():
    bpy.utils.unregister_class(RhinMostraOcultaFace)
    bpy.utils.unregister_class(RhinLinhaBase)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    bpy.utils.unregister_class(RhinPivoCursor)
    bpy.utils.unregister_class(RhinCriaEspessura)
    bpy.utils.unregister_class(RhinEsculturaGrab)
    bpy.utils.unregister_class(RhinRostoCriaCopia)
    bpy.utils.unregister_class(RhinDistanciaObjetos)
    bpy.utils.unregister_class(RhinZoomCena)
    bpy.utils.unregister_class(RhinCriaFotogrametria)
    bpy.utils.unregister_class(RhinImportaFotogrametria)
    bpy.utils.unregister_class(RhinAlinhaFaces)
    bpy.utils.unregister_class(RhinEstudaFaces)
    bpy.utils.unregister_class(RhinRedimensionamento)
    bpy.utils.unregister_class(RhinSeparaFace)
    bpy.utils.unregister_class(RhinEstudoEstrutura)
    bpy.utils.unregister_class(RhinEscultura)
    bpy.utils.unregister_class(RhinPrePos)
    bpy.utils.unregister_class(RhinDesenhaGuia)


if __name__ == "__main__":
    register()
