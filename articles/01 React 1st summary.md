
# React 01 1st summary

Ref:
+ [Every React Concept Explained in 12 Minutes](https://www.youtube.com/@TheCodeBootcamp)
+ [React18基础系列-05-我学到的useState4个细节丨讲师·景水](https://www.bilibili.com/video/BV1eP411a7gm/?spm_id_from=333.999.0.0&vd_source=6997c0a04f6a78d03d30de86e9b949d9)
todos:
- [ ] [React 原理解析](https://7km.top/main/macro-structure/)
## 基本文件 & 项目创建

### 白板

通过`npx create-next-app@latest`将含有一个babel的库，这库就是将你js函数含有html标签部分的返回值，渲染成真正的html。也就是==jsx语法==。

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```
对于这个`index.js`文件，我们找到html的根节点，然后通过`ReactDOM.createRoot`来创建一个虚拟的DOM节点，就是我们的==虚拟DOM==。

### vite 创建 & tailwindCSS & react-router-dom

+ 使用vite创建项目
```bash
npm create vite@latest name-of-your-project 
%% 之后可以按需求选择 %%
%% cd 进你的项目 %%
```

+ 安装router
```bash
npm install react-router-dom
```

+ 安装tailwindcss并进行初始化
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
需要对tailwindcss config进行配置
1. edit `tailwind.config.js`
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

2. edit `./src/index.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
3. 因为tailwind去除了一些基本样式，所以我还是建议导入`@tailwindcss/typography`这个包
```bash
npm install @tailwindcss/typography
```
```js
module.exports = {
  // ...
  plugins: [
    require('@tailwindcss/typography'),
    // ...
  ],
};
```
 [Tailwind CSS Typography 插件的文档](https://tailwindcss.com/docs/typography-plugin)


## 组件 & jsx语法

### 组件命名

+ 组件我们都统一大写首字母
+ 可以使用enclosing tag的方式，但是注意后面要空一格(如`Hello` 和` />` 之间有一个空格)
+ 导出的话必须要在一个tag之中，不能返回多个tag。如这里我们使用了一个空tag进行包裹，这也是jsx的特色
```jsx

const Hello = () => <div>Hello world</div>;

export default function App() {

  return (
    <>
	    <Hello />
    </>
  )
}
```

### jsx

jsx就是在js代码中写html
像上面那个Hello App一样，我们定义了一个App的函数他的返回值却是一个html

需要注意下面几点
+ 如果你在html需要传入一些值，或者表达式，就需要用`{}`包裹 
	`{theme === 'dark' ? 'light' : 'dark'}`
+ boolen 就不会显示了
	`{true false}`
### js 中的 array

+ react中使用map这种iterate操作需要给子元素一个unique的key值，以方便react在虚拟dom中快速操作。
```jsx
const arr = [1, 2, 3, 4, 5]
...
      <ul>
        arr.map((item) => {
            return <li key={item}>{item}</li>
            })
      </ul>
```

+ 例如上面的arr map之后应该是返回一个含有n个li tag的array，但是react会直接解构他们，最终结果就是ul tag 里面含有那几个 li tag
	`{[1, 2]}`会直接解构值出来


### trick: 样式设置

例如这里，我们需要对一个button做复杂的样式设计，我们就可以将样式赋值给一个变量，且将逻辑封装在里面
这样组件的属性和逻辑就一目了然
```jsx
import { PiSunDimFill } from "react-icons/pi";
import { BiSolidMoon } from "react-icons/bi";

const ThemeSwitch = () => {

  const switchClasses = `flex items-center justify-center w-6 h-6 text-dark bg-white rounded-full transform ${
    isActive ? "translate-x-0" : "translate-x-6"
  } transition-transform duration-500 ease-in-out`;

  return (
      <button className={switchClasses}>
        {isActive ? <PiSunDimFill size={16} /> : <BiSolidMoon />}
      </button>
  );
};

export default ThemeSwitch;

```

### trick: 条件反写

`{!arr.length && console.log('empty array')}`
直接`arr.length`会有个0跟在后面，所以用`!`进行boolen化还是有好处的

## 组件通信

### 值传递

例如我们为Container组件传入 value和handleclick两个值
```jsx
import Container from "../components/container"
import { useState } from "react"

export default function Home() {
	const arr = [1, 2, 3, 4, 5]
    const [state, setState] = useState(0)
  return (
    <div>
      <Container value={arr} handleclick={{state, setState}}/>
    </div>
  )
}
```


有两种接受方式

1. 直接设置一个props或者params参数接受所有传入值，以obj的方式调用他的值
```jsx
export default function Container(params) {
    console.log(params.value)
    console.log(params.handleclick)

  return (
    <div>
		
    </div>
  )
}
```



2. 在接收的时候就用对应名称解构参数，注意==名称一定要对的上==
```jsx
export default function Container({value, handleclick}) {
    console.log(value)
    console.log(handleclick)

  return (
    <div>
		
    </div>
  )
}
```


### 组件传递

以下面这个`Wrapper`组件为例，使用起来类似一个槽slug，将children填充。
>如果是不解构，可以同过`params.children`来访问，默认以array类型返回
```jsx
// 定义一个 Wrapper 组件
function Wrapper({ children }) {
  return <div className="wrapper">{children}</div>;
}

// 在使用 Wrapper 组件时，可以在其内部放置任何内容
function App() {
  return (
    <Wrapper>
      <h1>This is a title</h1>
      <p>This is a paragraph.</p>
    </Wrapper>
  );
}
```

![](http://sb0212bul.hn-bkt.clouddn.com/blogImages/20240329231520.png)
## 组件渲染 useState

### 渲染顺序

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```
一般来说，由于你的app在StrictMode下，组件会渲染两遍

可以观察下面的脚本
```jsx
import { useState } from "react"

export default function Home() {
    
    const [state, setState] = useState(0)
    const handleClick = () => {
      setState(state + 1)
      console.log(`func state${state}`)
    }
    
    console.log(`outer state${state}`)

  return (
    <div>
      <h1 className="text-2xl font-bold" >Hello world</h1>
      <button onClick={handleClick}>123</button>
    </div>
  )
}
```

可以看到console输出了两遍外部的state
```
outer state0
outer state0
```

如果你点击我们定义的button的话，就算是要求react来响应你的操作，于是它会更新这部分组件
```
func state0
outer state1
outer state1
```

+ `func state1`是由于我们点击产生的
+ `outer state2` × 2 则是因为restrict模式下的渲染


### 异步

从上面的例子可以观察到在`handleClick`内部的我们state值是没有更新的，到外面才更新

我们修改一下代码
```jsx
import { useState } from "react"

export default function Home() {
    
    const [state, setState] = useState(0)
    const handleClick = () => {
      setState(state + 1)
      setState(state + 1)
      setState(state + 1)
      console.log(`func state${state}`)
    }
    
    console.log(`outer state${state}`)

  return (
    <div>
      <h1 className="text-2xl font-bold" >Hello world</h1>
      <button onClick={handleClick}>123</button>
    </div>
  )
}
```

这里我们希望增加三次但是输出却还是一样的，也就是说func里面做了三遍0+1
```
func state0
outer state1
outer state1
```


解决方法：使用函数
```jsx
    const handleClick = () => {
      setState(state =>state + 1)
      setState(state =>state + 1)
      setState(state =>state + 1)
      
      console.log(`func state${state}`)
    }
```
由于我们在`setState`定义了一个箭头函数，那么这就是一个函数类型的`setState`(react的特殊设计)。

函数和非函数形式的`setState`:

1. **非函数形式的 `setState`:** 当您使用非函数形式的 `setState`（如 `setState(state + 1)`），React 会==批量==处理这些更新。
    
2. **函数形式的 `setState`:** 使用函数形式的 `setState`（如 `setState(state => state + 1)`），确保每次更新都是基于该状态的最新值。在这种情况下，即使在同一个事件处理函数中多次调用 `setState`，每次调用都会接收到前一次更新后的状态值。因此，函数形式的 `setState` 实际上是在==排队==，每个更新依次执行，并且每次都是基于最新的状态值。

这里有一个简化的比喻来解释这两种情况：

- **非函数形式的 `setState`:** 想象有三个人几乎同时告诉你要在一个计数器上加1，但是他们都没有查看当前的计数器值。你只会加1，因为所有的请求都是基于原始的计数器值。
    
- **函数形式的 `setState`:** 现在，想象这三个人一个接一个地告诉你加1，但是在每次操作之前，他们都会查看当前的计数器值。这样，你会连续加3，因为每个操作都是基于上一个人更新后的计数器值。

最后：其实也可以让handle里面强制同步，
```jsx
const handleClick = () => {
  let tmp = state + 1
  tmp = tmp + 1
  setState(tmp)
  
  console.log(`func state${state}`)
}
```

ps: 
```jsx
const handleClick = () => {
  setState(state =>state + 1)
  setState(state =>state + 1)
  setState(state =>state + 1)

  setState((state) => {
    console.log(`innerfunc state${state}`);
    return state;
  });

  console.log(`func state${state}`)
}
```

### 死循环

由于我们`setState`方法一改变state，我们的组件就会渲染。在一些情况下，我们的组件是会无限渲染的。


比如，直接在component内部调用了`setState`，可想而知：
1. 每次我们组件更新都是调用`setState`
2. 而`setState`又会改变state的值
3. state变了又会造成组件更新 (...回到第一步了)
4. 而`setState`又会改变state的值
5. ...

因此，任何时候你都不应该在函数的定义里面以任何方式调用setState。
==以一个简单的方式来检查：思考一遍渲染下来，你的setState不必被执行。==
那么就是没问题的。


## useEffect

> Strict Mode下useEffect 渲染的顺序: 

React 会先完成组件的渲染(包括 Strict Mode 引起的重复渲染),然后再处理 useEffect。
这个过程大致如下:

1. 组件第一次渲染
2. 组件第二次渲染(Strict Mode)
3. 处理第一次渲染的 useEffect
4. 处理第二次渲染的 useEffect


### 执行顺序

先整个组件渲染完成，然后来执行`useEffect`的内容，也就是说你可以在`useEffect`里面写一些获取渲染后的内容。
```jsx
import { useState } from "react";
import { useEffect } from "react";

export default function Home() {
    const [state, setState] = useState(0);

    useEffect( () => {
        console.log('in useEffect')
        console.log(document.querySelector('#title').textContent)
    })

    console.log('in component')

    return (
        <div>
            <h1 id="title" className="text-2xl font-bold">Hello world {state} </h1>
            <button onClick={() => setState(state + 1)}>Click me</button>
        </div>
    )
}
```

### 依赖项

`useEffect`的第二个参数就是依赖项：
+ 没写依赖项的话，每次render，我们的`useEffect`都是执行
+ 写入一个空列表，表示初始化的render完毕后，我们`useEffect`会执行，之后render都不会执行
+ 写入一个依赖项，表示每次依赖项更新，`useEffect`就会执行里面的函数，更新步骤如下：
	1. 依赖项变化，导致组件重新渲染
	2. 组件渲染完毕，`useEffect`工作 ，`useEffect`检测到依赖项变化
	3. useEffect工作


正常情况：
	当然，如果你在`useEffect`里面也有写一些`setState`等改变组件值的方法，又会重新激发组件render。render完之后，`useEffect`检测依赖项没有变化，大家就都歇着了。
无限渲染：
	让你设置`useEffect`依赖项，并且依赖项会在`useEffect`里面被set(改变)的时候，这将导致一个无限渲染循环。这是因为每次 `useEffect` 执行时更新状态都会触发组件的再次渲染，然后这个新的渲染会触发 `useEffect` 的又一次执行，如此往复。


### 清理阶段

> 使用场景：比如在useEffect中连接数据库，如果没有清理函数，会跟数据库保持多个连接。

+ useEffect 回调函数的返回值可以没有，有就必须是一个函数
+ 执行时机：
	1. 组件被销毁时
	2. 第二次执行回调时，先执行上一次回调中的返回值函数(先清理上一次)


## useContext

使用`useContext`为组件提供方便的值调用：
1. 使用`createContext`来实例化一个context对象
2. 使用`context.Provider`来包裹组件，并在==value属性(必须是value属性)==中添加你需要传入的值
	1. 例如provider包裹了A组件，A(B(C))，如此嵌套
	2. `<AppContext.Provider value={{state, setState}}>`
```jsx
import { createContext, useState } from "react";
import FirstContext from "./home/homecontext";

export const AppContext = createContext();

function App() {
  const [state, setState] = useState(0);

  return (
    <div className=" text-center mt-10">
        <AppContext.Provider value={{state, setState}}>
          <FirstContext />
        </AppContext.Provider>
    </div>
  );
}

export default App;
```
3. 在B / C组件中import 你创建的 context 实例 这里的AppContext，然后通过useContext来consume AppContext 以获取value属性的值
```jsx
import { AppContext } from "../App"
import { useContext } from "react"

export default function FirstContext() {
    const {state, setState} = useContext(AppContext)
    console.log(AppContext)
    return (
        <div>
            <h1>First Context</h1>
            <h2>State: {state}</h2>
            <button onClick={() => setState(state + 1)}>Increment</button>
        </div>
    )
}
```

## useRef

对比：
+ 相较于`useState`，`useRef`是一种更改值，但是不重新渲染组件的方法

使用：
+ 对tag的ref属性进行设置为`useRef`的值(例如aRef)进行标记这个tag，然后你就可以通过`aRef.current`获取被标记的tag，来进行dom操作
```jsx
import { useEffect, useRef } from "react";

export default function Search() {
  const inputRef = useRef(null);
  
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "/" && document.activeElement !== inputRef.current) {
        event.preventDefault();
        inputRef.current.focus();
      } else if (event.key === "Escape") {
        if (document.activeElement === inputRef.current) {
          inputRef.current.blur();
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return (
    <label className="h-10 w-auto pl-4 pr-2 bg-base-200 rounded-lg flex items-center gap-2 ">
      <input
        ref={inputRef}
        type="text"
        className="my-input w-14 focus:md:w-28 bg-base-200 outline-none transition-width duration-300 ease-in-out "
        placeholder="Search"
      />
      <kbd className="kbd kbd-sm bg-base-100 border font-semibold">/</kbd>
    </label>
  );
}

```

+ 另外还有一种将ref传递的方式，例如你想将ref绑定到子组件的某个组件，你就需要在子组件绑定一个`ref={yourRef}`，然后才能在子组件中给子子组件绑定`yourRef`。这可以通过使用 `React.forwardRef` 来实现，并在父组件中使用 `useRef` 钩子。
```jsx
import React, { useRef, forwardRef } from 'react';

// 子组件
const Child = forwardRef((props, ref) => (
  <div>
    <input ref={ref} />
  </div>
));

// 父组件
function Parent() {
  const inputRef = useRef();

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <div>
      <Child ref={inputRef} />
      <button onClick={handleClick}>Focus Input</button>
    </div>
  );
}
```
在父组件中,我们定义了一个 handleClick 函数。这个函数会在按钮被点击时调用。在这个函数内部,我们通过 inputRef.current 访问到了子组件内部的 input 元素,并调用了它的 focus 方法。

## useReducer

### 一般使用

`useReducer` 是一个 React 钩子（hook），它是 `useState` 的替代方案，适用于复杂的状态逻辑，尤其是当下一个状态依赖于之前的状态时。`useReducer` 还让你能够优化触发深度更新的组件，因为你可以传递调度（dispatch）而不是回调函数。

下面是一个使用 `useReducer` 的例子，这个例子是一个简单的计数器，它有增加和减少计数的功能：

```jsx
import React, { useReducer } from 'react';

// 定义初始状态
const initialState = { count: 0 };

// 定义reducer函数
// reducer函数接收当前状态和一个action对象，返回新的状态
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      throw new Error();
  }
}

function Counter() {
  // 使用useReducer钩子初始化reducer和初始状态
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </>
  );
}

export default Counter;
```

在这个例子中：

1. `initialState` 定义了计数器的初始状态，它是一个对象，包含一个名为 `count` 的属性。
2. `reducer` 函数是一个纯函数，它接受当前的状态和一个描述操作的 `action` 对象作为参数，然后根据 `action.type` 返回新的状态。在本例中，我们处理了两种类型的动作：`increment`（增加计数）和 `decrement`（减少计数）。
3. `useReducer` 钩子接收 `reducer` 函数和初始状态，并返回当前状态和一个 `dispatch` 函数。这个 `dispatch` 函数可以接受一个动作对象来触发状态的更新。
4. `Counter` 组件渲染当前的 `count` 值，并提供两个按钮，用户可以点击这些按钮来分别增加或减少计数。点击按钮时，会调用 `dispatch` 函数并传入一个包含 `type` 字段的对象来指定要执行的动作类型。

使用 `useReducer` 可以让你将组件的状态更新逻辑外置到 `reducer` 函数中，这样可以使逻辑更加清晰，也便于测试和复用。对于复杂组件或者有多个子值的状态对象，这种模式往往比 `useState` 更可取。

### 封装使用

您可以封装 `useReducer` 钩子以及相关的逻辑，创建自定义钩子。这样做可以让您在多个组件间复用状态逻辑，保持组件代码的整洁性，并且更好地分离关注点。

下面我们将上述计数器的例子中的逻辑封装成一个自定义钩子：

```jsx
import React, { useReducer } from 'react';

// 定义初始状态
const initialState = { count: 0 };

// 定义reducer函数
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      throw new Error();
  }
}

// 自定义钩子，封装了状态和调度函数
function useCounter(initialCount = 0) {
  const [state, dispatch] = useReducer(reducer, { count: initialCount });

  // 返回状态和用于修改状态的函数
  return {
    count: state.count,
    increment: () => dispatch({ type: 'increment' }),
    decrement: () => dispatch({ type: 'decrement' }),
  };
}

function Counter() {
  // 使用自定义钩子
  const { count, increment, decrement } = useCounter();

  return (
    <>
      Count: {count}
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
    </>
  );
}

export default Counter;
```

在这个封装后的例子中：

- `useCounter` 是一个自定义钩子，它使用 `useReducer` 内部维护状态，并且返回状态 `count` 以及两个函数 `increment` 和 `decrement` 用于改变状态。
- 初始计数值 `initialCount` 可以作为参数传递给 `useCounter` 钩子，这提供了灵活性，允许不同的组件实例可能有不同的初始值。
- 在 `Counter` 组件中，我们直接使用 `useCounter` 钩子提供的状态和函数，而不是直接与 `useReducer` 相关的逻辑打交道。

通过这种封装，您可以轻松地在多个组件间共享和重用计数器的逻辑，同时保持组件的简洁和可读性。每当您需要使用计数器逻辑时，只需调用 `useCounter` 钩子即可。



quick note:
+ useRef就是可以去操控dom元素，例如实现按下/ focus到input
+ portal和createPortal
+ suspend还可以设定你的lazy component，只有当组件真正要用的时候加载，其他的时候都是lazy

## 内存优化
### React.memo

在React中：
	父组件更新时，会trigger重新渲染，这时子组件会跟着渲染一遍
	而子组件更新时，只会trigger自己重新渲染
但是，当子组件并没有变化的时候，跟着父组件一起渲染，这是性能浪费。
且当子组件非常复杂时，性能损耗的大小就不可忽略了。

`React.memo` 是一个高阶组件，它用于对组件进行性能优化。当组件的props没有改变时，它可以阻止组件的重新渲染。这对于避免不必要的渲染是非常有用的，特别是在渲染成本较高的组件或有大量组件时。

下面是一个使用 `React.memo` 的例子：

```jsx
import React, { useState } from 'react';

// 一个简单的子组件，接受一个props：text
const MyComponent = React.memo(({ text }) => {
  console.log('MyComponent re-rendered');
  return <div>{text}</div>;
});

// 父组件
function App() {
  const [text, setText] = useState('');
  const [count, setCount] = useState(0);

  return (
    <div>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={() => setCount(count + 1)}>
        Click me ({count})
      </button>

      {/* MyComponent 组件使用 React.memo 包裹 */}
      <MyComponent text={text} />
    </div>
  );
}

export default App;
```

在这个例子中：

- `MyComponent` 是一个展示文本的简单组件。它通过 `React.memo` 被包裹，这意味着只有当它的 `text` props 发生变化时，组件才会重新渲染。
- `App` 是一个父组件，它有一个文本输入字段和一个按钮。文本输入用于更新 `MyComponent` 的 `text` props，而按钮则用于增加 `count` 状态，但并不直接影响 `MyComponent`。

在这个例子中，无论您点击按钮多少次，`MyComponent` 只会在其 `text` props 改变时重新渲染。如果您没有使用 `React.memo`，每次点击按钮时 `MyComponent` 都会重新渲染，即使它的 props 实际上并没有变化。

这个优化可以提升大型应用程序的性能，尤其是当避免深层次的组件树不必要的重新渲染时。然而，`React.memo` 只进行浅比较，所以如果您传递了一个复杂的对象作为 props，并且这个对象每次渲染时都是一个新的实例，即使实际上没有改变，`React.memo` 也会导致组件重新渲染。在这种情况下，您可能需要使用 `useMemo`、`useCallback` 或其他方法来避免不必要的渲染。


### useMemo

`useMemo` 是一个 React 钩子，用于返回一个记忆化的值。当你有一个计算成本较高的值，并且你不希望在每次组件渲染时都重新计算它时，`useMemo` 非常有用。通过使用 `useMemo`，React 会在依赖项没有改变的情况下，跳过这个值的重新计算，并从缓存中返回最近一次计算的值。

下面是一个使用 `useMemo` 的例子，其中包含了一个成本较高的计算（模拟情况）：

```jsx
import React, { useState, useMemo } from 'react';

function expensiveCalculation(num) {
  
  console.time('calculate')
  for (let i = 0; i < 1000000000; i++) {} // 假设这是一个耗时的操作
  console.timeEnd('calculate')
  return num * 2;
}

function App() {
  const [number, setNumber] = useState(0);
  const [isGreen, setIsGreen] = useState(true);

  // 使用useMemo来记忆计算结果，只有当number变化时才重新计算
  const doubledNumber = useMemo(() => {
    return expensiveCalculation(number);
  }, [number]);

  return (
    <div>
      <input
        type="number"
        value={number}
        onChange={(e) => setNumber(parseInt(e.target.value, 10))}
      />
      <h2
        onClick={() => setIsGreen(!isGreen)}
        style={{ color: isGreen ? 'limegreen' : 'crimson' }}
      >
        {doubledNumber}
      </h2>
    </div>
  );
}

export default App;
```

在这个例子中：

- `expensiveCalculation` 函数模拟了一个耗时的计算过程（这里是一个循环，但在实际应用中可能是一个复杂的算法）。
- `App` 组件有两个状态：`number` 和 `isGreen`。`number` 用于 `expensiveCalculation` 函数，而 `isGreen` 用于切换文本颜色。
- `useMemo` 钩子用于记忆 `expensiveCalculation` 函数的结果，并将 `number` 作为依赖项。这意味着只有当 `number` 变化时，计算才会重新执行；如果 `number` 未发生变化，则返回之前计算的缓存值。
- 当用户在输入框中输入数字时，`number` 状态会更新，导致 `useMemo` 重新计算 `doubledNumber`。
- 当用户点击 `<h2>` 元素时，`isGreen` 状态会切换，但是由于 `doubledNumber` 的值只取决于 `number`，`useMemo` 会返回之前缓存的 `doubledNumber`，而不会重新执行昂贵的计算。

使用 `useMemo` 可以提升性能，特别是当组件经常重新渲染，但依赖的数据并不经常变化时。这样可以避免不必要的计算，节省资源。


### useCallback





