>使用next的官网learn项目进行学习

# Nextjs 基础

## styling

### clsx

[clsx 切换样式](https://nextjs.org/learn/dashboard-app/css-styling#using-the-clsx-library-to-toggle-class-names)

+ 使用clsx将不变的样式参数作为第一个参数传入，并将需要改变的样式参数使用大括号包裹进行判断
```tsx
import clsx from 'clsx';
 
export default function InvoiceStatus({ status }: { status: string }) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-2 py-1 text-sm',
        {
          'bg-gray-100 text-gray-500': status === 'pending',
          'bg-green-500 text-white': status === 'paid',
        },
      )}
    >
    // ...
)}
```

## font & img

>[如何加载字体和图片](https://nextjs.org/learn/dashboard-app/optimizing-fonts-images#adding-a-primary-font) 
>font 和 img会作为静态资源被next加载，而不用请求，是框架的加速部分。

### 加载字体

需要两步：
1. 创建一个文件导入你需要的字体
```ts
import { Inter } from 'next/font/google';
 
export const inter = Inter({ subsets: ['latin'] });
```
2. 应用你的字体
```ts
import '@/app/ui/global.css';
import { inter } from '@/app/ui/fonts';
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>{children}</body>
    </html>
  );
}
```
注意这里使用的是tailwind css，使用一个类似模板字面量的方式插入值，另外antialiased也是一个tailwind 属性(让字体变平滑)

### 加载图片
1. 导入`Image`组件
2. 设置组件
> [注意此处使用了Tailwind的响应式组件](https://tailwindcss.com/docs/responsive-design) 当宽度大于764px的时候图片才会显示(md默认值)，即md时设置容器为 block显示模式
```ts
import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { lusitana } from '@/app/ui/fonts';
import Image from 'next/image';
 
export default function Page() {
  return (
    // ...
    <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12">
      {/* Add Hero Images Here */}
      <Image
        src="/hero-desktop.png"
        width={1000}
        height={760}
        className="hidden md:block"
        alt="Screenshots of the dashboard project showing desktop version"
      />
    </div>
    //...
  );
}
```

## route page & layout

### page

+ 你所创建每个路由都将由`page`页面导出(==page文件是必须的==)
	+ 例如：`/app/dashboard/page.tsx` is associated with the `/dashboard` path.
	+ This is how you can create different pages in `Next.js`: create a new route segment using a folder, and add a `page` file inside it.

### layout

+ 作为一个公共组件当前路径下所有的页面（即所有children都会继承这个组件
```tsx
import SideNav from '@/app/ui/dashboard/sidenav';
 
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="w-full flex-none md:w-64">
        <SideNav />
      </div>
      <div className="flex-grow p-6 md:overflow-y-auto md:p-12">{children}</div>
    </div>
  );
}
```
+ 部分渲染：One benefit of using layouts in `Next.js` is that on navigation, only the page components update while the layout won't re-render.

![](http://sb0212bul.hn-bkt.clouddn.com/blogImages/20240312211714.png)



## navigate

[客户端导航，部分渲染: This means, when a user navigates to a new route, the browser doesn't reload the page, and only the route segments that change re-render - improving the navigation experience and performance.](https://nextjs.org/docs/app/building-your-application/routing/linking-and-navigating#how-routing-and-navigation-works)

### Link

> 注意这里的arr含对象的数据形式，让程序的可读性增加
```tsx
import {
  UserGroupIcon,
  HomeIcon,
  DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';

const links = [
  { name: 'Home', href: '/dashboard', icon: HomeIcon },
  {
    name: 'Invoices',
    href: '/dashboard/invoices',
    icon: DocumentDuplicateIcon,
  },
  { name: 'Customers', href: '/dashboard/customers', icon: UserGroupIcon },
];

export default function NavLinks() {
  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          <Link
            key={link.name}
            href={link.href}
            className="flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3"
          >
            <LinkIcon className="w-6" />
            <p className="hidden md:block">{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
```

### show actived link

```tsx
'use client';
 
import {
  UserGroupIcon,
  HomeIcon,
  DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
 
// ...
 
export default function NavLinks() {
  const pathname = usePathname();
 
  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
              {
                'bg-sky-100 text-blue-600': pathname === link.href,
              },
            )}
          >
            <LinkIcon className="w-6" />
            <p className="hidden md:block">{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
```


## url跟踪和解析

+ `useSearchParams`For example, the search params for this URL `/dashboard/invoices?page=1&query=pending` would look like this: `{page: '1', query: 'pending'}`.
+ **`usePathname`** - For example, for the route `/dashboard/invoices`, `usePathname` would return `'/dashboard/invoices'`. 
- **`useRouter`** - Enables navigation between routes within client components programmatically. There are [multiple methods](https://nextjs.org/docs/app/api-reference/functions/use-router#userouter) you can use. [useRouter ref](https://nextjs.org/docs/app/api-reference/functions/use-router)
- `URLSearchParams` 提供了一组方便的方法来操作 URL 查询参数,使得在处理复杂的 URL 参数时更加简洁和直观。它可以帮助你避免手动拼接和解析查询字符串的繁琐过程,提高代码的可读性和可维护性。[URLSearchParams并不是next方法，见MDN](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams/URLSearchParams)

### 组建一个input search组件

```tsx
'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';

export default function Search({ placeholder }: { placeholder: string }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const {replace} = useRouter();

  function handleSearch(term: string) { 
    const params = new URLSearchParams(searchParams);
    if (term) {
      params.set('query', term);
    } else {
      params.delete('query');
    }
    replace(`${pathname}?${params.toString()}`)
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <input
        className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
        placeholder={placeholder}
        onChange={(e) => {handleSearch(e.target.value)}}
        defaultValue={searchParams.get('query')?.toString()}
      />
      <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
    </div>
  );
}

```
+ 使用`onChange`属性传入input里面的值value
+ 使用`useSearchParams`获取当前url的参数，使用`URLSearchParams`组成一个方便拼接的url字符串(使用它的set、delete功能)
	+ 将value设置给`URLSearchParams`的实例，params
+ 使用`useRouter`的replace方法代替当前的url
	+ 配合`usePathname`获取路径
+ `defaultValue={searchParams.get('query')?.toString()}`设置默认值，保证刷新时url和input一致

> 另外：page组件也接受一个searchParams参数，他的效果跟`useSearchParams`一样，可以获得查询参数，使用两者中的一个取决于你是client还是server(`useSearchParams`)

## fetching data

+ page页面是async component，即可以使用await
+ [vercel postgre SDK，如何使用vercel的数据库组件](https://vercel.com/docs/storage/vercel-postgres/sdk)
+ [这一节中记录的图表生成](https://nextjs.org/learn/dashboard-app/fetching-data#fetching-data-for-revenuechart) 
### Sql 语句解释
这段代码中的 SQL 查询是用于根据给定的查询条件和分页参数从数据库中获取过滤后的发票数据。让我逐步解释这个 SQL 查询:

```tsx
SELECT
  invoices.id,
  invoices.amount,
  invoices.date,
  invoices.status,
  customers.name,
  customers.email,
  customers.image_url
FROM invoices
JOIN customers ON invoices.customer_id = customers.id
WHERE
  customers.name ILIKE ${`%${query}%`} OR
  customers.email ILIKE ${`%${query}%`} OR
  invoices.amount::text ILIKE ${`%${query}%`} OR
  invoices.date::text ILIKE ${`%${query}%`} OR
  invoices.status ILIKE ${`%${query}%`}
ORDER BY invoices.date DESC
LIMIT ${ITEMS_PER_PAGE} OFFSET ${offset}
```

1. `SELECT` 子句:
   - 选择要返回的列,包括发票的 `id`、`amount`、`date`、`status`,以及客户的 `name`、`email` 和 `image_url`。

2. `FROM` 子句:
   - 指定要查询的主表为 `invoices` 表。

3. `JOIN` 子句:
   - 使用 `JOIN` 关键字将 `invoices` 表和 `customers` 表进行连接,连接条件是 `invoices.customer_id` 等于 `customers.id`,建立发票和客户之间的关系。

4. `WHERE` 子句:
   - 指定查询条件,使用 `ILIKE` 操作符对多个列进行模糊匹配。
   - `customers.name ILIKE ${`%${query}%`}`: 匹配客户名称中包含查询词的记录。
   - `customers.email ILIKE ${`%${query}%`}`: 匹配客户邮箱中包含查询词的记录。
   - `invoices.amount::text ILIKE ${`%${query}%`}`: 将发票金额转换为文本类型,然后匹配包含查询词的记录。
   - `invoices.date::text ILIKE ${`%${query}%`}`: 将发票日期转换为文本类型,然后匹配包含查询词的记录。
   - `invoices.status ILIKE ${`%${query}%`}`: 匹配发票状态中包含查询词的记录。
   - 使用 `OR` 关键字将这些条件进行组合,只要满足任意一个条件即可匹配。

5. `ORDER BY` 子句:
   - 按照 `invoices.date` 的降序对结果进行排序,最新的发票会显示在前面。

6. `LIMIT` 和 `OFFSET` 子句:
   - `LIMIT ${ITEMS_PER_PAGE}`: 限制返回的记录数量为 `ITEMS_PER_PAGE` 个。
   - `OFFSET ${offset}`: 指定偏移量,跳过前面的 `offset` 个记录,用于实现分页功能。

这个 SQL 查询通过连接 `invoices` 表和 `customers` 表,根据客户名称、邮箱、发票金额、日期和状态进行模糊匹配,并按照发票日期降序排序,同时使用 `LIMIT` 和 `OFFSET` 实现分页功能,返回过滤后的发票数据。

需要注意的是,查询条件中使用了模板字符串和占位符 `${...}` 来动态插入查询词和分页参数,这是为了防止 SQL 注入攻击。同时,使用 `::text` 将数值类型转换为文本类型,以便进行模糊匹配。


### 实时数据 unstable_noStore

+ [dynamic rather than use data in cache](https://nextjs.org/learn/dashboard-app/static-and-dynamic-rendering#making-the-dashboard-dynamic) 
```tsx
import { unstable_noStore as noStore } from 'next/cache';
 
export async function fetchLatestInvoices() {
  noStore();
  // ...
}
```


## streaming

### loading page & route group

+ 如果想当前路由的所有子页面都用这个loading可以将loading文件直接放在路由文件夹下
+ 如果只想用在当前路由页面，而除开子页面，可以创建`(overview)`文件夹，文件夹下放page和loading文件即可(也可以用其他名字)
	Route groups allow you to organize files into logical groups without affecting the URL path structure. When you create a new folder using parentheses `()`, the name won't be included in the URL path. So `/dashboard/(overview)/page.tsx` becomes `/dashboard`.

![](sb0212bul.hn-bkt.clouddn.com/blogImages/20240313230916.png)

+ 因为()可以用作对页面的包裹，你也可以用它来分类
  Here, you're using a route group to ensure `loading.tsx` only applies to your dashboard overview page. However, you can also use route groups to separate your application into sections (e.g. `(marketing)` routes and `(shop)` routes) or by teams for larger applications.
+ 公共布局的分类，如shop的layout跟marketing的layout可以分别作用在小组内
+ 隐式的页面组 ，进行功能划分

```
/app
  /(shop)
    /products
      /[id]/page.tsx
    /cart/page.tsx
    /checkout/page.tsx
  /(marketing)
    /about/page.tsx
    /contact/page.tsx
    /blog
      /[slug]/page.tsx
  /(account)
    /profile/page.tsx
    /orders/page.tsx
```

### suspend 
>滞后显示数据传输时间长的组件，让其他快的组件先显示


[代码示例](https://nextjs.org/learn/dashboard-app/streaming#streaming-a-component)
1. 将数据传输的调用 改到慢的组件之中
2. 使用`<Suspense> </Suspense>`将慢组件包裹


## 表单提交

### 表单的创建

+ 创建一个form tag 
+ 其action属性填入我们处理表单数据的组件
	+ `<form action={createInvoice}>` form所选的数据就会都传给组件处理了
+ label的for属性我们使用forhtml
+ option 我们也需要加入id属性
	+ 使用disable 来设置一个不可选的默认显示选项

下面引入一个典型的表单(列表选择，输入，选项勾选)
+ 注意下面的peer用法，让你所选的地方高亮以提高accessibility

![](sb0212bul.hn-bkt.clouddn.com/blogImages/20240314202130.png)

```tsx
    <form action={createInvoice}>
      <div className="rounded-md bg-gray-50 p-4 md:p-6">
        {/* Customer Name */}
        <div className="mb-4">
          <label htmlFor="customer" className="mb-2 block text-sm font-medium">
            Choose customer
          </label>
          <div className="relative">
            <select
              id="customer"
              name="customerId"
              className="peer block w-full cursor-pointer rounded-md border border-gray-200 py-2 pl-10 text-sm outline-2 placeholder:text-gray-500"
              defaultValue=""
            >
              <option value="" disabled>
                Select a customer
              </option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.name}
                </option>
              ))}
            </select>
            <UserCircleIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500" />
          </div>
        </div>

        {/* Invoice Amount */}
        <div className="mb-4">
          <label htmlFor="amount" className="mb-2 block text-sm font-medium">
            Choose an amount
          </label>
          <div className="relative mt-2 rounded-md">
            <div className="relative">
              <input
                id="amount"
                name="amount"
                type="number"
                step="0.01"
                placeholder="Enter USD amount"
                className="peer block w-full rounded-md border border-gray-200 py-2 pl-10 text-sm outline-2 placeholder:text-gray-500"
              />
              <CurrencyDollarIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
          </div>
        </div>

        {/* Invoice Status */}
        <fieldset>
          <legend className="mb-2 block text-sm font-medium">
            Set the invoice status
          </legend>
          <div className="rounded-md border border-gray-200 bg-white px-[14px] py-3">
            <div className="flex gap-4">
              <div className="flex items-center">
                <input
                  id="pending"
                  name="status"
                  type="radio"
                  value="pending"
                  className="h-4 w-4 cursor-pointer border-gray-300 bg-gray-100 text-gray-600 focus:ring-2"
                />
                <label
                  htmlFor="pending"
                  className="ml-2 flex cursor-pointer items-center gap-1.5 rounded-full bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-600"
                >
                  Pending <ClockIcon className="h-4 w-4" />
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="paid"
                  name="status"
                  type="radio"
                  value="paid"
                  className="h-4 w-4 cursor-pointer border-gray-300 bg-gray-100 text-gray-600 focus:ring-2"
                />
                <label
                  htmlFor="paid"
                  className="ml-2 flex cursor-pointer items-center gap-1.5 rounded-full bg-green-500 px-3 py-1.5 text-xs font-medium text-white"
                >
                  Paid <CheckIcon className="h-4 w-4" />
                </label>
              </div>
            </div>
          </div>
        </fieldset>
      </div>
      <div className="mt-6 flex justify-end gap-4">
        <Link
          href="/dashboard/invoices"
          className="flex h-10 items-center rounded-lg bg-gray-100 px-4 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-200"
        >
          Cancel
        </Link>
        <Button type="submit">Create Invoice</Button>
      </div>
    </form>
```

### 内存 & redirect

重点：
+ 在提交表单之后使用`revalidatePath`来清空滞后的当前url这部分路径所对应的内存
+ 同时使用`redirect`函数将用户导航到新建表单的位置
+ formData的数据狠多的话可以使用[entries](https://developer.mozilla.org/en-US/docs/Web/API/FormData/entries)
>zod是一个类似Pydantic对数据类型进行验证和转化的库

这里是上面的表单的数据传到这里进行处理，数据包裹成formData，且会在这里解包进行上传
```tsx
'use server';
 
import { sql } from '@vercel/postgres';
import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

const FormSchema = z.object({
  id: z.string(),
  customerId: z.string(),
  amount: z.coerce.number(),
  status: z.enum(['pending', 'paid']),
  date: z.string(),
});

const CreateInvoice = FormSchema.omit({ id: true, date: true });

export async function createInvoice(formData: FormData) {
    const { customerId, amount, status } = CreateInvoice.parse({
        customerId: formData.get('customerId'),
        amount: formData.get('amount'),
        status: formData.get('status'),
    })
    const amountInCents = amount * 100;
    const date = new Date().toISOString().split('T')[0];

    await sql`
    INSERT INTO invoices (customer_id, amount, status, date)
    VALUES (${customerId}, ${amountInCents}, ${status}, ${date})
    `;
    
    revalidatePath('/dashboard/invoices')
    redirect('/dashboard/invoices')
}
```


## 动态路由 和 参数传递

### 动态路由

使用这种结构`[id]/edit`invoices和edit中间的路径就可以为任意值

![](sb0212bul.hn-bkt.clouddn.com/blogImages/20240314222804.png)

### bind绑定对象

使用js的bind方法，将实例对象绑定，再传到组件中，值就可以保持不变

例如,我们定义一个delete button，button传入id，id交给`deleteInvoice`函数，在button传入id的时候绑定id(设置第一个参数为 `null`，这表示我们不需要绑定 `this` 的上下文)，这个id将作为第一个参数赋予对象
```tsx
<div className="flex justify-end gap-2">
	<DeleteInvoice id={invoice.id} />
</div>

export async function deleteInvoice(id: string) {
  await sql`DELETE FROM invoices WHERE id = ${id}`;
  revalidatePath('/dashboard/invoices');
}

export function DeleteInvoice({ id }: { id: string }) {
  const deleteInvoiceWithId = deleteInvoice.bind(null, id);

  return (
    <form action={deleteInvoiceWithId}>
      <button className="rounded-md border p-2 hover:bg-gray-100">
        <span className="sr-only">Delete</span>
        <TrashIcon className="w-4" />
      </button>
    </form>
  );
}
```

## handle errors

### catch error
+ 捕捉一般错误，可以使用js的`try...catch` 
+ 然后在页面同级目录创建`error.tsx`来自定义你的error 样式
	+ 如果子页面没有自己的error文件的话，他们的error会继承上一级文件的error
> 但是404的优先级更高，如果是访问不存在的页面，会优先404而非使用error页面

下面是一个实例
```tsx
export async function deleteInvoice(id: string) {
  throw new Error('Failed to Delete Invoice');
}
```

```tsx
'use client';
 
import { useEffect } from 'react';
 
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Optionally log the error to an error reporting service
    console.error(error);
  }, [error]);
 
  return (
    <main className="flex h-full flex-col items-center justify-center">
      <h2 className="text-center">Something went wrong!</h2>
      <button
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
        onClick={
          // Attempt to recover by trying to re-render the invoices route
          () => reset()
        }
      >
        Try again
      </button>
    </main>
  );
}
```

+ "use client" - `error.tsx` 需要是一个客户端组件。  
+ 它接受两个属性：  
	+ error：此对象是 JavaScript 原生 Error 对象的一个实例。  
	+ reset：这是一个用于重置错误边界的函数。当执行时，该函数将尝试重新渲染路由段。

### 404

+ 只需要创建`not-found.tsx`即可，子路由没有的话，继承关系也是一样的
+ 另外可以通过`notFound`函数手动捕捉到404页面
```tsx
import { fetchInvoiceById, fetchCustomers } from '@/app/lib/data';
import { updateInvoice } from '@/app/lib/actions';
import { notFound } from 'next/navigation';
 
export default async function Page({ params }: { params: { id: string } }) {
  const id = params.id;
  const [invoice, customers] = await Promise.all([
    fetchInvoiceById(id),
    fetchCustomers(),
  ]);
 
  if (!invoice) {
    notFound();
  }
 
  // ...
}
```

```tsx
import Link from 'next/link';
import { FaceFrownIcon } from '@heroicons/react/24/outline';
 
export default function NotFound() {
  return (
    <main className="flex h-full flex-col items-center justify-center gap-2">
      <FaceFrownIcon className="w-10 text-gray-400" />
      <h2 className="text-xl font-semibold">404 Not Found</h2>
      <p>Could not find the requested invoice.</p>
      <Link
        href="/dashboard/invoices"
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
      >
        Go Back
      </Link>
    </main>
  );
}
```


## validation

### require
最简单的给tag标记require，从而使得此项不能为空

### 使用zod

```jsx
import React, { useState } from 'react';
import { z } from 'zod';

// 创建一个 zod 方案，用于验证数字
const numberSchema = z.number();

function NumericInput() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const newValue = event.target.value;
    setValue(newValue);
    
    // 使用 zod 检查输入是否可以解析为数字
    const parseResult = numberSchema.safeParse(parseFloat(newValue));

    if (parseResult.success) {
      setError('');
    } else {
      setError('请输入数字');
    }
  };

  return (
    <div>
      <input
        type="text"
        value={value}
        onChange={handleChange}
        style={{ borderColor: error ? 'red' : 'initial' }}
      />
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}

export default NumericInput;
```



# 进阶

## 划分 server 和 client


### server 和 client 基本的定界
+ server部分的渲染应该尽可能的大部分，因为build时候server会尽可能变成静态html使得访问速度更快。（不标记`use client`，默认就是server
+ client部分应该尽可能细的划分，比如你有一个含有search-bar的layout页面，与其mark整个layout页面为client，不如把search-bar拿出去单独写一个`use client`然后在layout页面引入，这样就不用把整个layout组件发送给client，而只需要client部分的js代码
```tsx
// SearchBar is a Client Component
import SearchBar from './searchbar'
// Logo is a Server Component
import Logo from './logo'
 
// Layout is a Server Component by default
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <Logo />
        <SearchBar />
      </nav>
      <main>{children}</main>
    </>
  )
}
```


### 如果需要混合server和client
[reference](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns#supported-pattern-passing-server-components-to-client-components-as-props)
+ 如果你需要在client中使用server组件，不要直接import，而是通过props将server component作为props传到 client component
```jsx
'use client'
 
import { useState } from 'react'
 
export default function ClientComponent({
  children,
}: {
  children: React.ReactNode
}) {
  const [count, setCount] = useState(0)
 
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      {children}
    </>
  )
}
```

```jsx
// This pattern works:
// You can pass a Server Component as a child or prop of a
// Client Component.
import ClientComponent from './client-component'
import ServerComponent from './server-component'
 
// Pages in Next.js are Server Components by default
export default function Page() {
  return (
    <ClientComponent>
      <ServerComponent />
    </ClientComponent>
  )
}
```

With this approach, `<ClientComponent>` and `<ServerComponent>` are decoupled and can be rendered independently. ==In this case, the child `<ServerComponent>` can be rendered on the server, well before `<ClientComponent>` is rendered on the client.==

+ 如果你需要从client组件传递参数到server组件
	1. 在client的children中设置一个参数`{children(count)}`
	2. 在server组件中接受这个参数
	3. 在组合页面中，使用箭头函数传递这个参数给组件`{(count) => <ServerComponent count={count} />}`
```jsx
// app/client-component.tsx
'use client'
 
import { useState } from 'react'
 
export default function ClientComponent({
  children,
}: {
  children: (data: number) => React.ReactNode
}) {
  const [count, setCount] = useState(0)
 
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      {children(count)}
    </>
  )
}

// app/server-component.tsx
export default function ServerComponent({ count }: { count: number }) {
  return <p>Current count: {count}</p>
}

// app/page.tsx 
import ClientComponent from './client-component'
import ServerComponent from './server-component'
 
export default function Page() {
  return (
    <ClientComponent>
      {(count) => <ServerComponent count={count} />}
    </ClientComponent>
  )
}
```

### 关于children 参数传递

在将 Server Component 传递给 Client Component 时,你不仅限于使用 children prop,还可以使用任何其他的 prop 来传递 JSX。

在 React 中,有一些特殊的 prop 具有特定的功能:

1. children: 这是最常见的一个特殊 prop。它允许你将 JSX 元素直接传递给组件,这些元素会被渲染在组件的内部某个位置。例如:
```jsx
<MyComponent>
  <div>This is the children prop</div>
</MyComponent>
```

2. key: 这个 prop 在列表渲染中非常重要。它帮助 React 识别哪些项目已更改、添加或删除。key 应该在数组内是唯一的。
3. ref: 这个 prop 允许你直接访问 DOM 元素或组件实例。
4. dangerouslySetInnerHTML: 这个 prop 允许你设置元素的 innerHTML。因为它容易导致 XSS 攻击,所以被称为 "dangerously"。

除了这些特殊的 prop,你可以传递任何自定义的 prop 来传递数据,包括回调函数,这些 prop 没有特殊的功能,仅用于数据传递。

例如,你可以使用自定义的 prop 而不是 children 来传递 JSX:
```jsx
<ClientComponent serverComponent={<ServerComponent />} />
```

然后在 ClientComponent 中,你可以渲染 serverComponent prop:
```jsx
function ClientComponent({ serverComponent }) {
  return (
    <div>
      {serverComponent}
    </div>
  );
}
```


## fetching data

### 按需重验证 revalidate

>注意revalidate是因为你cache了数据，如果你cache: 'no-store' 自然每次都是新的

[revalidate on-demand](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating#on-demand-revalidation)
1. 使用fetch时，给需要的fetch标记一个tags
2. 使用`revalidateTag`来激活你需要重新validate的部分
```jsx
export default async function Page() {
  const res = await fetch('https://...', { next: { tags: ['collection'] } })
  const data = await res.json()
  // ...
}
```

```jsx
'use server'
 
import { revalidateTag } from 'next/cache'
 
export default async function action() {
  revalidateTag('collection')
}
```

### useFormState

+ 这是个react的方法，相当于是useState
+ 还有一个useFormStatus 
```jsx
'use server'
 
export async function createUser(prevState: any, formData: FormData) {
  // ...
  return {
    message: 'Please enter a valid email',
  }
}
```

```jsx
'use client'
 
import { useFormState } from 'react-dom'
import { createUser } from '@/app/actions'
 
const initialState = {
  message: '',
}
 
export function Signup() {
  const [state, formAction] = useFormState(createUser, initialState)
 
  return (
    <form action={formAction}>
      <label htmlFor="email">Email</label>
      <input type="text" id="email" name="email" required />
      {/* ... */}
      <p aria-live="polite" className="sr-only">
        {state?.message}
      </p>
      <button>Sign up</button>
    </form>
  )
}
```


# Appendix

### debug nextjs in vscode
>[debug ref](https://nextjs.org/docs/pages/building-your-application/configuring/debugging)
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev",
      "serverReadyAction": {
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "action": "debugWithChrome"
      }
    }
  ]
}
```


## 目录设置

[项目组织和文件托管](https://nextjs.org/docs/app/building-your-application/routing/colocation)

> update，应该使用如下目录，lib和ui最好放在app外，保持app里面都是建好的页面，非常干净。
```
src
├── app
│   ├── dashboard
|   ...
│   ├── page.tsx
│   └── layout.tsx
├── lib 
├── ui (component)
```
--------

出路`app/`下的页面路由`dashboard/`等，应该有`ui`,`lib`的设置
+ ui下面的分级类似你页面面的工具，相当于是存了一些封装的组件
+ lib的设置为了整个项目的工作提供一些小脚本

例如下面的app/下的目录分类
+ ui的customers、dashboard、invoices跟页面设置的dashboard文件夹是意义对应的，ui中的这些文件夹为dashboard文件夹中的页面提供封装好的ui组件
+ 模组导入使用`@`符号`import Form from '@/app/ui/invoices/create-form';`
	+ 在 Next.js 中,`@` 符号是一个特殊的别名,用于指向==项目根目录==。它是 Next.js 提供的一种方便的路径别名(path alias)功能。它允许你使用绝对路径来导入模块,而不必关心当前文件相对于根目录的位置。
	+ 使用src目录的话，在ts config中会将`"@/*": ["./src/*"]`做映射
+ 建议使用如下目录
```bash
.
├── dashboard
│   ├── (overview)
│   ├── customers
│   ├── invoices
│   ├── login
│   └── layout.tsx
├── lib
│   ├── action.tsx
│   ├── data.ts
│   ├── definitions.ts
│   ├── placeholder-data.js
│   └── utils.ts
└── ui
│   ├── customers
│   ├── dashboard
│   ├── invoices
│   ├── acme-logo.tsx
│   ├── button.tsx
│   ├── fonts.ts
│   ├── global.css
│   ├── login-form.tsx
│   ├── search.tsx
│   └── skeletons.tsx
├── page.tsx
├── layout.tsx
```

