export default {
  namespace: 'products',    // namespace 表示在全局 state 上的 key
  state: [],                // 初始值
  reducers: {               // 等同于 redux 里的 reducer，接收 action，同步更新 state
    'delete'(state, {payload: id}) {
      return state.filter(item => item.id !== 0)
    }
  }
}
