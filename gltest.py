import pyglet
from pyglet import shapes

class Snake():
	def __init__(self, x, y, nodes = []):
		self.vec_changed = False
		self.head = [x, y]
		self.vec = [0,1]
		self.nodes = nodes.copy() #These are the hitboxes
		if len(self.nodes) > 0:
			self.tail = self.nodes[0]

	def add_node(self, node):
		self.nodes.append(node)

	def rm_node(self, node = 0):
		return self.nodes.pop(node)

	def tail_update(self):
		tx, ty = self.tail
		if len(self.nodes) > 1:
			x, y = self.nodes[1]
		else:
			x, y = self.head

		if y == ty:
			#they are on the same y plane
			if tx - x == 0:
				print([tx, ty], [x, y], "TEST")
				print(self.nodes)
				return True
			elif tx - x > 0:
				print("a")
				tx -= 1
				self.tail[0] -= 1
			else:
				print("b")
				tx += 1
				self.tail[0] += 1
		else:
				#they are on the same x plane
			if ty - y == 0:
				return True
			elif ty - y > 0:
				ty -= 1
				self.tail[1] -= 1
			else:
				y += 1
				self.tail[1] += 1
		if [tx, ty] == [x, y]:
			return True
		return [[tx, ty], [x,y]]

	@property 
	def curr_node(self):
		return self.nodes[len(self.nodes)-1]

	def extend_nodes(self, li):
		self.nodes.extend(li)

	def __getitem__(self, key):
		return self.nodes[key]

	def __len__(self):
		return len(self.nodes)


class Game(object):
	def __init__(self, size = 5):
		self.window = pyglet.window.Window()
		self.batch = pyglet.graphics.Batch()
		self.size = size
		self.snake = Snake(40, 50, nodes = [[20, 40], [40, 40]])
		self.lines = [] #These hold the pyglet vertexlist objects
		self.apple = [70, 70]

		if len(self.snake) > 0: 
			for pos in range(0, len(self.snake.nodes) - 1):
				self.add_line(self.create_vertexlist(self.snake[pos], self.snake[pos+ 1]))
			self.head = self.create_vertexlist(self.snake[len(self.snake) - 1], self.snake.head)
		else:
			self.head = self.create_vertexlist(self.snake.head)

	def create_vertexlist(self, startVertex, endVertex = None):
		size = self.size
		if endVertex == None:
			endVertex = [startVertex[0] + 1, startVertex[1]]

		x, y = startVertex[0] * size, startVertex[1] * size,
		l, h = endVertex[0] * size, endVertex[1] * size
		if x == l:
			if h > y:
				return shapes.Rectangle(x, y, size, (h - y), batch = self.batch)
			else:
				return shapes.Rectangle(x, h, size, ((y - h)+ size), batch = self.batch)
		elif y == h:
			if l > x:
				return shapes.Rectangle(x, y, (l - x), size, batch = self.batch)
			else:
				return shapes.Rectangle(l, y, ((x - l)) + size, size, batch = self.batch)
		else:
			print("Error, rectangle being written not on the same plane: XY: ", startVertex, " lh: ", endVertex)

	def add_line(self, line):
		self.lines.append(line)

	def rm_line(self, pos= 0 ):
		self.lines[pos].delete()
		del self.lines[pos]
		self.snake.rm_node()


	def tail_update(self):
		packet = self.snake.tail_update()
		#boolean (if the snake's end was popped) and coordinates for new tail
		if isinstance(packet, bool):
		#	
		#if there are more nodes tht are 
			self.rm_line()
			self.snake.tail = self.snake[0]

		if isinstance(packet, list):
			if len(self.lines) == 0:
				"set the tail to be the size of the "
				self.snake.add_node(self.snake.head.copy())
				self.add_line(self.create_vertexlist(self.snake.head, self.snake.curr_node))
			if isinstance(self.lines[0], pyglet.shapes.Rectangle):
				print(packet)
				self.lines[0].delete()
				self.lines[0] = self.create_vertexlist(packet[0], packet[1])

	def head_update(self):

		self.head.delete()
		if len(self.snake) > 0:
			#print(self.snake.head, self.snake.curr_node)
			self.head = self.create_vertexlist(self.snake.head, self.snake.curr_node)
		else:
			print("this should never run")
			self.head = self.create_vertexlist(self.snake.head)

		self.snake.head[0] += self.snake.vec[0]
		self.snake.head[1] += self.snake.vec[1]

	def collision(self):
		if len(self.snake) > 2:
			# snake head will attach to end of nodes. 
			#that means that you should start from 0, and check till the end
			for pos in range(0, len(self.snake) - 2):
				#x collision
				if self.snake.head[0] == self.snake[pos][0] and self.snake.head[0] == self.snake[pos + 1][0]:
					if abs(self.snake[pos][1] - self.snake[pos + 1][1]) >= abs(self.snake[pos][1] - self.snake.head[1]):
					# if distance between y nodes is greater than distance between y and snake
						return True
				#y collision
				elif self.snake.head[1] == self.snake[pos][1] and self.snake.head[1] == self.snake[pos + 1][1]:
					if abs(self.snake[pos][0] - self.snake[pos + 1][0]) >= abs(self.snake[pos][0] - self.snake.head[0]):
						return True
		return False

	def apple_collision(self):
		if self.snake.head == self.apple:
			return True
		return False

	def frame_update(self, dt):
		if self.snake.vec == [0,0]:
			return 0

		#print(self.lines)
		if self.snake.vec_changed:
			#snake needs to be updated
			#vertex needs to be updated
			print("Node added", self.snake.head)
			self.add_line(self.create_vertexlist(self.snake.head, self.snake.curr_node))
			self.snake.add_node(self.snake.head.copy())
			self.snake.vec_changed = False

		self.head_update()

		if self.snake.tail != None:
			self.tail_update()

		if self.collision():
			print("COLLIDED")



game = Game()

@game.window.event
def on_draw():
	game.window.clear()
	game.batch.draw()

@game.window.event
def on_key_press(symbol, modifiers):
	conditional_mod = None
	if symbol == pyglet.window.key.UP:
		conditional_mod = [0, 1]
	if symbol == pyglet.window.key.DOWN:
		conditional_mod = [0, -1]
	if symbol == pyglet.window.key.RIGHT:
		conditional_mod = [1, 0]
	if symbol == pyglet.window.key.LEFT:
		conditional_mod = [-1, 0]

	if conditional_mod != None:
		if game.snake.vec[0] != conditional_mod[0] or game.snake.vec[1] != conditional_mod[1]:
		#if the vec isn't alr going up/down or left/ right
			game.snake.vec = conditional_mod
			game.snake.vec_changed = True



pyglet.clock.schedule_interval(game.frame_update, 0.1)
pyglet.app.run()
