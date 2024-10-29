bl_info = {
    "name": "Material Tools - 選択マテリアルノードを初期状態で複製",
    "author": "Yamaguchi",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "Node Editor > Right-click menu",
    "description": "シェーダーエディタ内で選択中のマテリアルノードを初期状態で複製します。マテリアルノードを選択し、右クリックメニュー→Material Tools→選択ノードを初期状態で複製",
    "warning": "",
    "category": "Node",
}

import bpy

class NODE_OT_clone_initial_state(bpy.types.Operator):
    bl_idname = "node.clone_initial_state"
    bl_label = "選択ノードを初期状態で複製"
    bl_description = "選択したマテリアルノードを初期状態で複製します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 選択中のノードツリーを取得
        material = context.object.active_material
        node_tree = material.node_tree
        selected_nodes = [node for node in node_tree.nodes if node.select]

        # 選択ノードが1つ以上あるかを確認
        if selected_nodes:
            for node in selected_nodes:
                # ノードのタイプを取得
                node_type = node.bl_idname

                # 新しいノードを追加（初期状態で）
                new_node = node_tree.nodes.new(type=node_type)

                # 元のノードの位置に配置
                new_node.location = (node.location.x + 200, node.location.y)
                new_node.select = False  # クローン元ノードの選択を解除
                node.select = False  # 元のノードの選択を解除
                new_node.select = True  # 新しいノードを選択

            self.report({'INFO'}, "複製成功")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "マテリアルノードが選択されていません。")
            return {'CANCELLED'}

# 自作のMaterial Toolsサブメニューを定義（ユニークなIDを使用）
class NODE_MT_material_tools_custom(bpy.types.Menu):
    bl_label = "Material Tools"
    bl_idname = "NODE_MT_material_tools_custom"  # 独自のIDを設定

    def draw(self, context):
        layout = self.layout
        layout.operator(NODE_OT_clone_initial_state.bl_idname)

# コンテキストメニューに自作の「Material Tools」サブメニューを追加
def menu_func(self, context):
    # 自作のMaterial Toolsサブメニューを常に追加
    self.layout.menu(NODE_MT_material_tools_custom.bl_idname)

# アドオンの登録と登録解除
def register():
    bpy.utils.register_class(NODE_OT_clone_initial_state)
    bpy.utils.register_class(NODE_MT_material_tools_custom)
    bpy.types.NODE_MT_context_menu.append(menu_func)  # NODE_MT_context_menuに追加

def unregister():
    bpy.utils.unregister_class(NODE_OT_clone_initial_state)
    bpy.utils.unregister_class(NODE_MT_material_tools_custom)
    bpy.types.NODE_MT_context_menu.remove(menu_func)  # NODE_MT_context_menuから削除

if __name__ == "__main__":
    register()